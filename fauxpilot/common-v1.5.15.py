#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import json
import os
import random
import string
import time

import requests
from cachetools import cached, TTLCache

from utils.tree_sitter import TreeSitterUtil
from utils.constant import FrontLanguageEnum, VueTagConst
from config import conf
from config.log_config import logger
from tokenizers import Tokenizer
import re

# Create a cache that can store up to 100 results, each with a lifetime of 30 minutes
cache = TTLCache(maxsize=1000, ttl=30 * 60)

SPECIAL_MIDDLE_SIGNAL = "<special-middle>"

# Define regular expression for CSS properties, supporting multi-line property values
css_property_pattern = re.compile(r'^\s*[a-zA-Z-]+\s*:\s*[^;]+;\s*$', re.MULTILINE)
# Define regular expression for CSS selectors
css_selector_pattern = re.compile(r'^\s*[.#]?[a-zA-Z0-9_-]+\s*\{', re.MULTILINE)
# Define regular expression for CSS comments
css_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
# Define regular expression for multi-line CSS properties
multiline_css_property_pattern = re.compile(r'^\s*[a-zA-Z-]+\s*:\s*[^;]+;\s*$', re.DOTALL | re.MULTILINE)


# Use the @cached decorator to cache function results
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
#                 "text": 'Qianliu Copilot authentication failed, please set the Token in the plugin settings page, \nYou can get the token from the settings page of Qianliu AI web version https://chat.sangfor.com.',
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
    Used to filter out Python code issues in non-Python language completions
    :params text: Code segment returned by completion
    """
    python_text_rules = os.environ.get("PYTHON_TEXT_RULES", 'return self.name').split(',')
    for text_rule in python_text_rules:
        if text_rule in text:
            logger.info(f"{text} is_python_text")
            return True


def init_tree_sitter(language, prefix, suffix):
    if language == FrontLanguageEnum.VUE.value:
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
        # Process the original prefix and suffix of the completion content, extract new prefix and suffix
        # (make the concatenated context as complete as possible to improve the hit rate of syntax correction)
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
    Process the prefix and suffix of the completion content, extract new prefix and suffix
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
    Process the prefix and suffix at the cursor position of the completion for more accurate prefix and suffix
    :param sitter:
    :param prefix:
    :param suffix:
    :return:
    """
    code = prefix + SPECIAL_MIDDLE_SIGNAL + suffix
    source_code = code.encode("utf-8")
    line_num, _ = get_choices_text_line_number(code, SPECIAL_MIDDLE_SIGNAL)

    # Locate the block node where the cursor belongs and parse the code block
    cur_block_code = sitter.get_node_text(source_code,
                                          sitter.find_second_level_node_by_line_num(source_code, line_num))

    # Locate the nearest previous and next nodes without syntax errors to the block node where the cursor belongs, and parse the code blocks respectively
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
    Get paired symbols and their corresponding mappings
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
    }


def get_quotes_symbols():
    return {
        '"': '"',
        "'": "'"
    }


def get_boundary_symbols():
    return ['{', '(', '[', '"', "'", ':', "<", ';', ',', '>', '.', '`']


def count_paired_symbols(text):
    """
    Count paired symbols
    :param text:
    :return:
    """
    symbols_map = {}
    for char in text:
        # Ignore isolated right brackets
        if char in get_right_paired_symbols() and symbols_map.get(get_right_paired_symbols()[char], 0) == 0:
            continue

        # Count paired symbols
        if char in get_paired_symbols():
            symbols_map[char] = symbols_map.get(char, 0) + 1

    return symbols_map


def remove_strings(code_line):
    """
    Remove strings from code line
    :param code_line:
    :return:
    """
    in_string = False
    string_char = None
    result = []

    for i, char in enumerate(code_line):
        if char in ['"', "'"]:
            if not in_string:
                in_string = True
                string_char = char
                result.append(char)
            elif string_char == char and (i == 0 or code_line[i-1] != '\\'):
                in_string = False
                string_char = None
                result.append(char)
        elif not in_string:
            result.append(char)

    return ''.join(result)


def is_cursor_in_parentheses(prefix, suffix):
    """
    Determine if the cursor is inside parentheses
    :param prefix:
    :param suffix:
    :return:
    """
    def find_parenthesis(text, symbol, is_reverse=False):
        """
        Find the position of a parenthesis
        :param text:
        :param symbol:
        :param is_reverse:
        :return:
        """
        search_text = text[::-1] if is_reverse else text
        quote_map = {
            '"': False,
            "'": False
        }

        symbol_stack = []
        paired_symbols = get_paired_symbols()

        for index, char in enumerate(search_text):
            if char in ['"', "'"]:
                quote_map[char] = not quote_map[char]
            if any(quote_map.values()):
                continue
            if char == symbol and not symbol_stack:
                return index if not is_reverse else len(text) - index - 1
            elif is_reverse:
                if char in paired_symbols.values():
                    opposite_char = get_right_paired_symbols()[char]
                    symbol_stack.append(opposite_char)
                elif char in paired_symbols and symbol_stack and symbol_stack[-1] == char:
                    symbol_stack.pop()
            else:
                if char in paired_symbols:
                    symbol_stack.append(char)
                elif char in paired_symbols.values() and symbol_stack and get_left_paired_symbols()[symbol_stack[-1]] == char:
                    symbol_stack.pop()

        return -1

    return find_parenthesis(prefix, '(', is_reverse=True) != -1 and find_parenthesis(suffix, ')') != -1


def is_cursor_in_string(cursor_prefix):
    """
    Determine if the cursor is inside a string
    :param cursor_prefix:
    :return:
    """
    in_double_quotes = False
    in_single_quotes = False
    escape_char = False

    for char in cursor_prefix:
        if escape_char:
            escape_char = False
            continue

        if char == '\\':
            escape_char = True
        elif char == '"' and not in_single_quotes:
            in_double_quotes = not in_double_quotes
        elif char == "'" and not in_double_quotes:
            in_single_quotes = not in_single_quotes

    return in_double_quotes or in_single_quotes


def get_choices_text_line_number(code, pattern):
    """
    Get the line numbers where the pattern appears in the code
    :param code:
    :param pattern:
    :return:
    """
    lines = code.split('\n')
    pattern_indices = []

    for i, line in enumerate(lines):
        if pattern in line:
            pattern_indices.append(i)

    if len(pattern_indices) >= 2:
        return pattern_indices[0], pattern_indices[1]
    return -1, -1


def isolated_prefix_suffix(code, pattern):
    """
    Extract prefix and suffix by pattern
    :param code:
    :param pattern:
    :return:
    """
    if pattern in code:
        parts = code.split(pattern)
        if len(parts) >= 3:
            prefix = parts[0]
            suffix = parts[2]
            return prefix, suffix
    return None, None


def vue_to_html_ts(prefix, suffix):
    """
    Convert Vue template to HTML for TreeSitter parsing
    :param prefix:
    :param suffix:
    :return:
    """
    if not prefix and not suffix:
        return FrontLanguageEnum.HTML.value, prefix, suffix

    # Try to determine if it's a <script> or <template> tag
    new_prefix = prefix
    for tag in [VueTagConst.TEMPLATE.value, VueTagConst.SCRIPT.value, VueTagConst.STYLE.value]:
        tag_start = f"<{tag}"
        tag_end = f"</{tag}>"

        if tag_start in prefix and tag_end in suffix:
            if tag == VueTagConst.TEMPLATE.value:
                return FrontLanguageEnum.HTML.value, new_prefix, suffix
            elif tag == VueTagConst.SCRIPT.value:
                return FrontLanguageEnum.JAVASCRIPT.value, new_prefix, suffix
            elif tag == VueTagConst.STYLE.value:
                return FrontLanguageEnum.CSS.value, new_prefix, suffix

    # If no specific tag is found, assume it's HTML by default
    return FrontLanguageEnum.HTML.value, prefix, suffix


def cache_clear():
    """
    Clear the cache
    """
    cache.clear()


def get_completion_cache_key(prompt):
    """
    Get cache key for completion
    """
    return hashlib.md5(prompt.encode('utf-8')).hexdigest()


def completion_make_cache(cache, completion_cache_time, prompt, text):
    """
    Cache completion results
    """
    if completion_cache_time <= 0:
        return
    cache_key = get_completion_cache_key(prompt)
    logger.info("completion_make_cache key:{} val:{}".format(cache_key, text))
    cache[cache_key] = {'val': text, 'expired_timestamp': int(time.time()) + completion_cache_time}


def get_completion_cache(cache, completion_cache_time, prompt):
    """
    Get completion results from cache
    """
    if completion_cache_time <= 0:
        return None
    cache_key = get_completion_cache_key(prompt)
    logger.info("get_completion_cache key:{}".format(cache_key))

    if cache_key in cache:
        # Check if the cache has expired
        expired_timestamp = cache[cache_key].get('expired_timestamp', 0)
        if int(time.time()) <= expired_timestamp:
            val = cache[cache_key]['val']
            if val:
                logger.info("cache:{} hit".format(cache_key))
                return val
        else:
            # Remove expired cache
            logger.info("cache:{} expired".format(cache_key))
            del cache[cache_key]
    return None


def compute_prefix_suffix_match_length(content):
    """
    Compute the length of the match between prefix and suffix
    """
    if len(content) <= 1:
        return 0
    for i in range(len(content) - 1, 0, -1):
        if content[:i] == content[-i:]:
            return i
    return 0


def is_repetitive_content(content):
    """
    Check if the content is repetitive
    """
    if not content or len(content) <= 4:
        return False
    lines = content.split('\n')
    if len(lines) >= 5:
        slice_size = len(lines) // 3
        return lines[:slice_size] == lines[slice_size:2*slice_size] or lines[slice_size:2*slice_size] == lines[2*slice_size:]
    return False


def is_repetitive(content):
    """
    Check if the content is repetitive
    """
    if not content:
        return False

    # Check for repetition of content
    content_length = len(content)
    half_length = content_length // 2

    return content[:half_length] == content[half_length:2*half_length]


def contains_only_non_alpha(input_string):
    """
    Check if the string contains only non-alphabetic characters
    """
    return all(not c.isalpha() for c in input_string)


def check_context_include_text(text, prefix, suffix):
    """
    Verify if text is the end part of the preceding context, and if it is the beginning part of the following context
    or exists in the following content with twice the number of lines as text
    """
    text_lines = text.split('\n')
    prefix_lines = prefix.split('\n')
    suffix_lines = suffix.split('\n')

    if len(text_lines) <= 2:
        return False

    # Check if text is part of prefix
    min_length = min(len(text_lines), len(prefix_lines))
    if min_length > 0 and text_lines[:min_length] == prefix_lines[-min_length:]:
        return True

    # Check if text is part of suffix
    min_length = min(len(text_lines), len(suffix_lines))
    if min_length > 0 and text_lines[-min_length:] == suffix_lines[:min_length]:
        return True

    # Check if text is included in suffix with at least twice the lines
    if len(suffix_lines) >= 2 * len(text_lines):
        suffix_text = '\n'.join(suffix_lines[:2*len(text_lines)])
        if text in suffix_text:
            return True

    return False


def cut_suffix_overlap(text, prefix, suffix, cut_suffix_line=3):
    """
    Cut off overlapping content between text and suffix
    """
    if not suffix:
        return text

    text_lines = text.split('\n')
    suffix_lines = suffix.split('\n')

    # If the number of suffix lines is less than the cut threshold, directly handle without cutting
    if len(suffix_lines) < cut_suffix_line:
        for i in range(len(text_lines)):
            if i < len(text_lines) and i < len(suffix_lines) and text_lines[-(i+1):] == suffix_lines[:i+1]:
                return '\n'.join(text_lines[:-(i+1)])
    else:
        # Get the first few lines of suffix to determine if they match with the end of text
        first_suffix_lines = suffix_lines[:cut_suffix_line]

        # Check if text ends with any part of the first few lines of suffix
        for i in range(len(first_suffix_lines), 0, -1):
            check_suffix = '\n'.join(first_suffix_lines[:i])
            if text.endswith(check_suffix):
                # Remove the overlapping part
                text = text[:-len(check_suffix)]
                break

    return text


def cut_repetitive_text(text):
    """
    Cut repetitive text
    """
    if not text:
        return text

    lines = text.split('\n')
    result_lines = []

    i = 0
    while i < len(lines):
        # Add the current line
        result_lines.append(lines[i])

        # Check if this line is repeated in the next lines
        repeated_count = 0
        j = i + 1
        while j < len(lines) and lines[j] == lines[i]:
            repeated_count += 1
            j += 1

        # Skip the repeated lines (maximum of 1 repetition)
        i += min(2, repeated_count + 1)

    return '\n'.join(result_lines)


def do_cur_repetitive_text(text, ratio=0.15):
    """
    Process currently repetitive text
    """
    words = re.findall(r'\w+', text.lower())
    word_count = {}

    for word in words:
        if len(word) >= 2:  # Only count words with at least 2 characters
            word_count[word] = word_count.get(word, 0) + 1

    # Find the most frequently occurring word
    most_common_word = max(word_count.items(), key=lambda x: x[1], default=('', 0))

    if most_common_word[1] > 1:
        # Calculate the repetition ratio
        repetition_ratio = most_common_word[1] / len(words) if words else 0

        if repetition_ratio > ratio:
            # Extract a non-repetitive part of the text
            lines = text.split('\n')

            if len(lines) >= 3:
                # Return the first 1/3 of the content if it's highly repetitive
                return '\n'.join(lines[:len(lines)//3])
            else:
                # For shorter content, just return the first line
                return lines[0] if lines else ""

    return text


def get_repetitive_rate(text):
    """
    Get the repetition rate of text
    """
    if not text:
        return 0

    words = re.findall(r'\w+', text.lower())
    word_count = {}

    for word in words:
        if len(word) >= 2:  # Only count words with at least 2 characters
            word_count[word] = word_count.get(word, 0) + 1

    # Find the most frequently occurring word
    most_common_word = max(word_count.items(), key=lambda x: x[1], default=('', 0))

    # Calculate the repetition ratio
    repetition_ratio = most_common_word[1] / len(words) if words else 0

    return repetition_ratio


def judge_css(language, text, ratio=0.7):
    """
    Determine if the text is CSS
    """
    if language != FrontLanguageEnum.CSS.value:
        lines = text.split('\n')
        css_line_count = sum(1 for line in lines if include_css(line))
        total_lines = len(lines)

        # If more than 70% of the lines match CSS patterns, consider it CSS
        if total_lines > 0 and css_line_count / total_lines >= ratio:
            return True

    return False


def include_css(line):
    """
    Check if a line includes CSS
    """
    # Remove CSS comments
    line = css_comment_pattern.sub('', line)

    # Check if it's a CSS property declaration (e.g., color: red;)
    if css_property_pattern.match(line):
        return True

    # Check if it's a CSS selector (e.g., .class-name {)
    if css_selector_pattern.match(line):
        return True

    # Check if it might be part of a multi-line CSS property
    if multiline_css_property_pattern.match(line):
        return True

    return False


def is_valid_brackets(text):
    """
    Check if brackets in the text string are complete
    """
    stack = []
    brackets_map = {"(": ")", "[": "]", "{": "}"}

    for char in text:
        if char in brackets_map:
            stack.append(char)
        elif char in brackets_map.values():
            if not stack or brackets_map[stack.pop()] != char:
                return False

    return len(stack) == 0


def is_valid_content(text):
    """
    Check if the content is valid
    """
    return is_valid_brackets(text)


def get_tokenizer_path(model_name, default_path):
    """
    Get the tokenizer path
    """
    tokenizer_path = os.environ.get(f"TOKENIZER_{model_name}", default_path)
    return tokenizer_path


def load_tokenizer(tokenizer_path):
    """
    Load the tokenizer
    """
    if not os.path.exists(tokenizer_path):
        return None
    return Tokenizer.from_file(tokenizer_path)
