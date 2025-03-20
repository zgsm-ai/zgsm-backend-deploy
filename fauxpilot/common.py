#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import json
import os
import random
import string

import requests
from cachetools import cached, TTLCache

from utils.tree_sitter import TreeSitterUtil
from utils.constant import LanguageConst, VueTagConst
from config import conf
from config.log_config import logger
from tokenizers import Tokenizer

# Create a cache, caching up to 100 results, with each result having a lifetime of 30 minutes
cache = TTLCache(maxsize=1000, ttl=30 * 60)

SPECIAL_MIDDLE_SIGNAL = "<special-middle>"


# Use the @cached decorator to cache the results of the function
# @cached(cache)
# def check_api_key(authorization):
#     if authorization:
#         url = conf['chatgpt_server_base_url'] + '/api/users/key'
#         api_key = authorization.replace("Bearer ", "")
#         response = requests.get(url, headers={'api-key': api_key})
#         if response.status_code in [200, 500, 504]:
#             return True, ''
#     completion = {
#         "id": random_completion_id(),
#         "choices": [
#             {
#                 "text": '千流 Copilot authentication failed. Please set the Token on the plugin settings page.\nYou can go to the Qianliu AI web version https://chat.sangfor.com settings page to obtain the token.',
#             }
#         ]
#     }
#     return False, json.dumps(completion)

def check_api_key(authorization):
    return True, ''

def random_completion_id():
    return 'cmpl-' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(29))


def is_python_text(text):
    """
    Used to filter out the issue of Python code appearing in non-Python language completions
    :params text: The code segment returned by the completion
    """
    python_text_rules = os.environ.get("PYTHON_TEXT_RULES", 'return self.name').split(',')
    for text_rule in python_text_rules:
        if text_rule in text:
            logger.info(f"{text} is_python_text")
            return True


def init_tree_sitter(language, prefix, suffix):
    if language == LanguageConst.VUE:
        language, prefix, suffix = vue_to_html_ts(prefix, suffix)
    try:
        sitter = TreeSitterUtil(language)
        return sitter
    except Exception as e:
        logger.error(f"Failed to initialize tree_sitter:", e)
        return None


def cut_text_by_tree_sitter(language, choices_text, prefix, suffix, time_start, time_out_threshold):
    """
    :params data: Interface parameters
    :params text: Code completion string
    """
    try:
        sitter = init_tree_sitter(language, prefix, suffix)
        if sitter is None:
            return choices_text
        # Process the original prefixes and suffixes of the completed content to extract new prefixes and suffixes (as much as possible to make the spliced context complete, and improve the hit rate of syntax correction)
        # prefix, suffix = extract_block_prefix_suffix(sitter, choices_text, prefix, suffix)
        new_prefix, new_suffix = extract_accurate_block_prefix_suffix(sitter, prefix, suffix)
        choices_text = sitter.intercept_syntax_error_code(choices_text, new_prefix, new_suffix,
                                                          time_start, time_out_threshold)
    except Exception as e:
        logger.error(f"Failed to cut {language} code:", e)
    return choices_text


def is_code_syntax(language, code, prefix, suffix):
    try:
        sitter = init_tree_sitter(language, prefix, suffix)
        if sitter is None:
            return True
        new_prefix, new_suffix = extract_accurate_block_prefix_suffix(sitter, prefix, suffix)
        return sitter.is_code_syntax(new_prefix + code + new_suffix)
    except Exception as e:
        logger.error(f"Failed to determine {language} code syntax error:", e)
    return True


def extract_block_prefix_suffix(sitter, choices_text, prefix, suffix):
    """
    Process the prefixes and suffixes of the completed content to extract new prefixes and suffixes
    :param sitter:
    :param choices_text:
    :param prefix:
    :param suffix:
    :return:
    """
    code = prefix + SPECIAL_MIDDLE_SIGNAL + choices_text + SPECIAL_MIDDLE_SIGNAL + suffix
    start_number, end_number = get_choices_text_line_number(code, SPECIAL_MIDDLE_SIGNAL)
    block_node = sitter.find_nearest_block(code.encode("utf-8"), start_number, end_number)
    code = sitter.get_node_text(code.encode("utf-8"), block_node)
    new_prefix, new_suffix = isolated_prefix_suffix(code, SPECIAL_MIDDLE_SIGNAL)
    if new_prefix and new_suffix:
        return new_prefix, new_suffix
    return prefix, suffix


def extract_accurate_block_prefix_suffix(sitter, prefix, suffix):
    """
    Process the prefixes and suffixes of the cursor position where the completion is located to extract more accurate prefixes and suffixes
    :param sitter:
    :param prefix:
    :param suffix:
    :return:
    """
    code = prefix + SPECIAL_MIDDLE_SIGNAL + suffix
    source_code = code.encode("utf-8")
    line_num, _ = get_choices_text_line_number(code, SPECIAL_MIDDLE_SIGNAL)

    # Locate the block node to which the cursor belongs and parse the code block
    cur_block_code = sitter.get_node_text(source_code,
                                          sitter.find_second_level_node_by_line_num(source_code, line_num))

    # Locate the nearest non-syntax error front and rear nodes of the block node to which the cursor belongs, and parse the code blocks respectively
    prefix_node, suffix_node = sitter.find_second_level_nearest_node_by_line_num(code.encode("utf-8"), line_num)
    prefix_block_code = sitter.get_node_text(source_code, prefix_node)
    suffix_block_code = sitter.get_node_text(source_code, suffix_node)

    new_code = "\n".join([prefix_block_code, cur_block_code, suffix_block_code])
    new_prefix, new_suffix = isolated_prefix_suffix(new_code, SPECIAL_MIDDLE_SIGNAL)
    if new_prefix and new_suffix:
        return new_prefix, new_suffix
    return prefix, suffix


def get_paired_symbols():
    """
    Get symbols that appear in pairs and the corresponding mappings
    :return:
    """
    return get_left_paired_symbols() | get_right_paired_symbols()


def get_right_paired_symbols():
    return {v: k for k, v in get_left_paired_symbols().items()}


def get_left_paired_symbols():
    return {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }


def get_quotes_symbols():
    return {
        '"': '"',
        "'": "'"
    }


def get_boundary_symbols():
    return ['{', '(', '[', '"', "'", ':', "<", ';']


def count_paired_symbols(text):
    """
    Count the symbols that appear in pairs
    :param text:
    :return:
    """
    symbols_map = {}
    for char in text:
        if char in get_paired_symbols():
            symbols_map[char] = symbols_map.get(char, 0) + 1
    return symbols_map


def remove_strings(code_line):
    """
    Delete the part of the code line that contains strings (the part enclosed in '' or "")
    :param code_line:
    :return:
    """
    result = []
    in_string = False
    quote_char = None
    buffer = []

    for char in code_line:
        if not in_string:
            if char in get_quotes_symbols():
                in_string = True
                quote_char = char
            else:
                result.append(char)
        else:
            if char == quote_char:
                in_string = False
                quote_char = None
                buffer = []
            else:
                buffer.append(char)
    if in_string:
        result.extend(buffer)
    return ''.join(result)


def is_cursor_in_parentheses(prefix, suffix):
    """
    Determine whether the cursor is in parentheses
    :param prefix:
    :param suffix:
    :return:
    """
    def find_parenthesis(text, symbol, is_reverse=False):
        """
         Find the subscript position of the non-paired symbol in the string text
        :param text:
        :param symbol:
        :param is_reverse:
        :return:
        """
        count = 0
        if is_reverse:
            text = text[::-1]
        for i in range(0, len(text)):
            if text[i] == get_paired_symbols()[symbol]:
                count += 1
            if text[i] == symbol:
                if count <= 0:
                    return i
                count -= 1
        return -1
    for left_symbol, right_symbol in get_left_paired_symbols().items():
        left_parenthesis_index = find_parenthesis(prefix, left_symbol, is_reverse=True)
        right_parenthesis_index = find_parenthesis(suffix, right_symbol, is_reverse=False)
        if left_parenthesis_index != -1 and right_parenthesis_index != -1:
            return True
    return False


def is_cursor_in_string(cursor_prefix, cursor_suffix):
    """
    Determine whether the cursor is in the string
    :param cursor_prefix:
    :param cursor_suffix:
    :return:
    """
    # Calculate the number of quotes in the prefix, ignoring escaped quotes
    quotes_count = {k: 0 for k in get_quotes_symbols()}
    i = 0
    while i < len(cursor_prefix):
        if cursor_prefix[i] == '\\':  # Skip escape characters
            i += 2
            continue
        if cursor_prefix[i] in get_quotes_symbols():
            quotes_count[cursor_prefix[i]] += 1
        i += 1

    # If the number of quotes is odd, the cursor is in the string
    for count in quotes_count.values():
        if count % 2 == 1:
            return True
    return False


def get_choices_text_line_number(code, pattern):
    """
    Get the line number of the completed content in the code
    :param code:
    :param pattern
    :return:
    """
    code_split = code.split("\n")
    start_number = 0
    end_number = 0
    for i in range(len(code_split)):
        if pattern in code_split[i] and start_number == 0:
            start_number = i
            continue

        if pattern in code_split[i] and start_number != 0:
            end_number = i
            break
    return start_number, end_number


def isolated_prefix_suffix(code, pattern):
    """
    Separate prefixes and suffixes
    :param pattern:
    :param code:
    :return:
    """
    if not code:
        return None, None

    spilt = code.split(pattern)
    if spilt and len(spilt) >= 2:
        return spilt[0], spilt[-1]
    return None, None


# Cut the vue code into html and ts code
def vue_to_html_ts(prefix, suffix):
    """
    :params prefix: Code block in front of the cursor
    :params suffix: Code block after the cursor
    """
    language = LanguageConst.VUE
    if (f"\n{VueTagConst.TS_START}" in prefix or prefix.startswith(VueTagConst.TS_START)) and (
            VueTagConst.TS_END in suffix or not suffix.strip()):
        language = LanguageConst.TS
        # Find the position of "<script>", and truncate prefix
        if prefix.startswith(VueTagConst.TS_START):
            prefix_index = prefix.find(VueTagConst.TS_START)
        else:
            prefix_index = prefix.find(f"\n{VueTagConst.TS_START}")
        if prefix_index != -1:
            # logger.info(f"{prefix_index} {prefix} xxx {prefix[prefix_index:]}")
            prefix = prefix[prefix_index:]
            # Delete the first line with \n as the line break symbol
            prefix = '\n'.join(prefix.strip().split('\n')[1:])
        # Find the position of "</script>", and truncate suffix
        suffix_index = suffix.find(VueTagConst.TS_END)
        # If "</script>" is found, delete it and the code behind it
        if suffix_index != -1:
            suffix = suffix[:suffix_index]
    elif (f"\n{VueTagConst.HTML_START}" in prefix or prefix.startswith(VueTagConst.HTML_START)) and (
            VueTagConst.HTML_END in suffix or not suffix.strip()):
        language = LanguageConst.HTML
        # The html part comes with a template tag
        prefix_index = prefix.find(VueTagConst.HTML_START)
        if prefix_index != -1:
            prefix = prefix[prefix_index:]
        suffix_index = suffix.find(VueTagConst.HTML_END)
        if suffix_index != -1:
            suffix = suffix[:suffix_index] + VueTagConst.HTML_END
    else:
        # If "<script>" or "<template>" is not found, return the original code block
        pass

    return language, prefix, suffix


# Clear cache
def cache_clear():
    cache.clear()


def get_completion_cache_key(prompt):
    hash_object = hashlib.sha256()
    hash_object.update(prompt.encode('utf-8'))
    return hash_object.hexdigest()


def completion_make_cache(cache, completion_cache_time, prompt, text):
    """
    @param: prompt Preprocessed promt
    @param: choices The result returned by the request model
    """
    if not cache.enabled:
        return
    hash_key = get_completion_cache_key(prompt)
    cache.set(hash_key, json.dumps(text))
    cache.expire(hash_key, completion_cache_time)


def get_completion_cache(cache, completion_cache_time, prompt):
    if not cache.enabled:
        return []
    hash_key = get_completion_cache_key(prompt)
    text = cache.get(hash_key)
    if text and len(text):
        # Renew
        cache.expire(hash_key, completion_cache_time)
        return json.loads(text)
    else:
        return []


STR_PREFIX_CONFIG = [
    {
        "maxTokenSequenceLength": 1,
        "lastTokensToConsider": 10,
    },
    {
        "maxTokenSequenceLength": 10,
        "lastTokensToConsider": 30,
    },
    {
        "maxTokenSequenceLength": 20,
        "lastTokensToConsider": 45,
    },
    {
        "maxTokenSequenceLength": 30,
        "lastTokensToConsider": 60,
    },
]


def compute_prefix_suffix_match_length(content):
    """
    Calculate the longest prefix suffix matching length of the string
    :param content: string
    :return: Matching length array
    """
    match_lengths = [0 for _ in range(len(content))]
    match_lengths[0] = -1
    match_index = -1
    for i in range(1, len(content)):
        while match_index >= 0 and content[match_index + 1] != content[i]:
            match_index = match_lengths[match_index]
        if content[match_index + 1] == content[i]:
            match_index += 1
        match_lengths[i] = match_index
    return match_lengths


def is_repetitive_content(content):
    match_lengths = compute_prefix_suffix_match_length(content)
    for config in STR_PREFIX_CONFIG:
        # Consider the number of duplicate characters in the prefix and suffix of the string composed of the last lastTokensToConsider characters
        max_match = max(match_lengths[:config["lastTokensToConsider"]])
        if (
            len(content) >= config["lastTokensToConsider"]
            and config["lastTokensToConsider"] - 1 - max_match <= config["maxTokenSequenceLength"]
        ):
            return True
    return False


def is_repetitive(content):
    """
    Determine whether the end of the string is repetitive content
    The calculation rules refer to https://devops.atrust.sangfor.com/demand/research_develop/3580/issues/695246
    :param content: String content
    :return: Whether it is repetitive content
    """
    return is_repetitive_content(content[::-1]) or \
        is_repetitive_content("".join(filter(lambda s: len(s.strip()) > 0, reversed(content))))


def contains_only_non_alpha(input_string):
    # Determine whether the string contains only non-alphabetic characters
    return all(not c.isalpha() for c in input_string)


def check_context_include_text(text, prefix, suffix):
    # Verify whether the text is the end of the upper context, and whether it is the beginning of the lower context or the number of lines in the lower context content is twice the content in the text
    if not text.strip():
        return True
    if len(text.strip()) <= 3 and suffix.strip().startswith(text.strip()[0]):
        # Analyze es data and find that the 1~2+line break character scenario is the same as the beginning of the lower context, it is considered the end of the upper context, and most scenarios are completions; ' ); etc., directly return empty
        return True
    if contains_only_non_alpha(text) and suffix.strip().startswith(text.strip()[0]):
        # Analyze es data. When text only has symbols and the lower context starts with the first non-empty character of text, it is considered the end of the upper context, and most scenarios are completions; ' ); etc., directly return empty
        # https://devops.atrust.sangfor.com/demand/research_develop/3580/issues/797264
        return True
    if text and len(text) <= 5:
        return False
    trimmed_text = text.strip()
    trimmed_prefix = prefix.strip()

    line_count = len(text.split("\n"))
    double_text = "\n".join(suffix.strip().split("\n")[:line_count * 2])
    if trimmed_prefix.endswith(trimmed_text):
        return True
    elif double_text.startswith(trimmed_text):
        return True
    elif line_count > 2 and trimmed_text in double_text:
        # When the number of returned lines is small, it is easy to misjudge. Add line number conditions here
        # https://devops.atrust.sangfor.com/demand/research_develop/3580/issues/815665
        return True
    else:
        return False


def cut_suffix_overlap(text, prefix, suffix, cut_suffix_line=3):
    """
    Remove the prefix overlap between the "completed content" and the suffix
    :param text: Completed content
    :param prefix: Upper context
    :param suffix: Lower context
    :param cut_suffix_line: The number of lines to intercept the suffix
    :return:
    """
    if not text:
        return text

    text = text.rstrip()
    text_len = len(text)
    suffix = suffix.strip()

    # Loop multiple times, each time cutting off the first line of the suffix and then performing content overlap cutting (the reason for looping multiple times is: the LLM defect may cause the text to overlap with the later content of the suffix)
    for _ in range(cut_suffix_line):
        new_text = text
        spilt_suffix = suffix.split("\n")
        suffix_len = len(suffix)
        if text_len == 0 or suffix_len == 0:
            return new_text

        first_line_suffix_len = len(spilt_suffix[0])
        max_overlap_length = min(text_len, suffix_len)
        for i in range(max_overlap_length, int(max_overlap_length / 2), -1):
            # If the length of the first line of suffix is greater than the de-duplication length, return directly
            if i < first_line_suffix_len:
                break
            # If the length of the first line of suffix is equal to the de-duplication length and the first line has only one word, there is no need to de-duplicate and return directly
            if i == first_line_suffix_len and len(suffix[:i].split(" ")) == 1:
                break

            # Once there is an overlap between text and suffix, return immediately
            if new_text[text_len - i:] == suffix[:i]:
                return new_text[:text_len - i]
        suffix = "\n".join(spilt_suffix[1:])
    return text


def cut_repetitive_text(text):
    """
    Remove duplicate content in the completed content
    :param text:
    :return:
    """
    if not text:
        return text

    # De-duplication is only triggered when the number of lines exceeds 3 (the premise of this strategy is: if the model starts to repeat at length, the content generated by the model usually has many lines)
    line_count = len(text.split("\n"))
    if line_count < 3:
        return text
    return do_cur_repetitive_text(text, ratio=0.15)


def do_cur_repetitive_text(text, ratio=0.15):
    """
    If the ratio of the longest prefix suffix matching length exceeds the threshold ratio, remove the duplicate content in the completed content
    :param text:
    :param ratio:
    :return:
    """
    if not text:
        return text

    # Calculate how many \n are at the end of text
    last_line_count = 0
    for i in range(len(text) - 1, -1, -1):
        if text[i] == '\n':
            last_line_count += 1
        else:
            break

    # Reverse the completed text
    text = text.rstrip()[::-1]

    # Calculate the longest prefix suffix length of the current reversed completed text
    max_match_lengths = max(max(compute_prefix_suffix_match_length(text)), 0)

    # If the longest prefix suffix length/completed content length is greater than or equal to ratio, it is judged as repetitive content
    if max_match_lengths > 0 and max_match_lengths / len(text) >= ratio:
        text = text[max_match_lengths + 1:]

    text = text[::-1]

    # Restore \n
    for i in range(last_line_count):
        text = text + "\n"
    return text


def is_valid_brackets(text):
    # Used to determine whether the brackets in the text string are complete
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in text:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        elif char in mapping.values():
            stack.append(char)
    return not stack


def get_tokenizer_path(model_name, default_path):
    model_env_var = f"{model_name.upper()}_MODEL"
    model_dir = os.environ.get(model_env_var, 'starcoder')
    tokenizer_path = f"/models/{model_dir}/tokenizer.json"
    return tokenizer_path if os.path.exists(tokenizer_path) else default_path


def load_tokenizer(tokenizer_path):
    try:
        return Tokenizer.from_file(tokenizer_path)
    except Exception as e:
        print(f"Error loading tokenizer from {tokenizer_path}: {e}")
        return None
