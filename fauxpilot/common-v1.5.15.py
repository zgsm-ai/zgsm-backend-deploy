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
from utils.constant import FrontLanguageEnum, VueTagConst
from config import conf
from config.log_config import logger
from tokenizers import Tokenizer
import re

# 创建一个缓存，最多缓存 100 个结果，每个结果的生命周期为 30 分钟
cache = TTLCache(maxsize=1000, ttl=30 * 60)

SPECIAL_MIDDLE_SIGNAL = "<special-middle>"

# 定义CSS属性的正则表达式，支持多行属性值
css_property_pattern = re.compile(r'^\s*[a-zA-Z-]+\s*:\s*[^;]+;\s*$', re.MULTILINE)
# 定义CSS选择器的正则表达式
css_selector_pattern = re.compile(r'^\s*[.#]?[a-zA-Z0-9_-]+\s*\{', re.MULTILINE)
# 定义CSS注释的正则表达式
css_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
# 定义多行CSS属性的正则表达式
multiline_css_property_pattern = re.compile(r'^\s*[a-zA-Z-]+\s*:\s*[^;]+;\s*$', re.DOTALL | re.MULTILINE)


# 使用 @cached 装饰器来缓存函数的结果
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
#                 "text": '千流 Copilot认证失败，请到插件设置页面设置Token，\n可前往千流AI网页版 https://chat.sangfor.com 设置页面获取token.',
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
    用于过滤非python语言补全出现python代码问题
    :params text: 补全返回的代码段
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
        logger.error(f"初始化tree_sitter失败:", e)
        return None

def cut_text_by_tree_sitter(language, choices_text, prefix, suffix, time_start, time_out_threshold):
    """
    :params data: 接口参数
    :params text: 代码补全字符串
    """
    try:
        sitter = init_tree_sitter(language, prefix, suffix)
        if sitter is None:
            return choices_text
        # 对补全内容的原始前后缀进行处理，抽取出新的前后缀（尽可能使得拼接后的上下文完整，提高语法修正的命中率）
        # prefix, suffix = extract_block_prefix_suffix(sitter, choices_text, prefix, suffix)
        new_prefix, new_suffix = extract_accurate_block_prefix_suffix(sitter, prefix, suffix)
        choices_text = sitter.intercept_syntax_error_code(choices_text, new_prefix, new_suffix,
                                                          time_start, time_out_threshold)
    except Exception as e:
        logger.error(f"切割{language}代码失败:", e)
    return choices_text


def is_code_syntax(language, code, prefix, suffix):
    try:
        sitter = init_tree_sitter(language, prefix, suffix)
        if sitter is None:
            return True
        new_prefix, new_suffix = extract_accurate_block_prefix_suffix(sitter, prefix, suffix)
        return sitter.is_code_syntax(new_prefix + code + new_suffix)
    except Exception as e:
        logger.error(f"判断{language}代码语法错误失败:", e)
    return True


def extract_block_prefix_suffix(sitter, choices_text, prefix, suffix):
    """
    对补全内容的前后缀进行处理，抽取出新的前后缀
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
    对补全所在光标位置的前后缀进行处理，抽取出更加准确的前后缀
    :param sitter:
    :param prefix:
    :param suffix:
    :return:
    """
    code = prefix + SPECIAL_MIDDLE_SIGNAL + suffix
    source_code = code.encode("utf-8")
    line_num, _ = get_choices_text_line_number(code, SPECIAL_MIDDLE_SIGNAL)

    # 定位到光标所属block结点，解析出代码块
    cur_block_code = sitter.get_node_text(source_code,
                                          sitter.find_second_level_node_by_line_num(source_code, line_num))

    # 定位到光标所属block结点的最近无语法错误的前后结点，分别解析出代码块
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
    获取成对出现的符号以及对应的映射
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
    统计成对出现的符号
    :param text:
    :return:
    """
    symbols_map = {}
    for char in text:
        # 忽略孤立的右括号
        if char in get_right_paired_symbols() and symbols_map.get(get_right_paired_symbols()[char], 0) == 0:
            continue
        if char in get_paired_symbols():
            symbols_map[char] = symbols_map.get(char, 0) + 1
    return symbols_map


def remove_strings(code_line):
    """
    删除代码行中包含字符串的部分（用''或用""括起来的部分）
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
    判断光标是否在括号内
    :param prefix:
    :param suffix:
    :return:
    """

    def find_parenthesis(text, symbol, is_reverse=False):
        """
         找到字符串text中非成对出现的symbol的下标位置
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

def is_cursor_in_string(cursor_prefix):
    """
    判断光标是否在字符串内
    :param cursor_prefix:
    :return:
    """
    # 计算前缀中的引号数量，忽略转义的引号
    quotes_count = {k: 0 for k in get_quotes_symbols()}
    i = 0
    while i < len(cursor_prefix):
        if cursor_prefix[i] == '\\':  # 跳过转义字符
            i += 2
            continue
        if cursor_prefix[i] in get_quotes_symbols():
            quotes_count[cursor_prefix[i]] += 1
        i += 1

    # 如果引号数量为奇数，则光标在字符串内
    for count in quotes_count.values():
        if count % 2 == 1:
            return True
    return False


def get_choices_text_line_number(code, pattern):
    """
    获取补全内容在代码中的行号
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
    分离前后缀
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


# 将vue代码切分为html和ts代码
def vue_to_html_ts(prefix, suffix):
    """
    :params prefix: 光标前面代码块
    :params suffix: 光标后面代码块
    """
    language = FrontLanguageEnum.VUE
    if (f"\n{VueTagConst.TS_START}" in prefix or prefix.startswith(VueTagConst.TS_START)) and (
            VueTagConst.TS_END in suffix or not suffix.strip()):
        language = FrontLanguageEnum.TS
        # 查找"<script>"的位置,对prefix进行截取
        if prefix.startswith(VueTagConst.TS_START):
            prefix_index = prefix.find(VueTagConst.TS_START)
        else:
            prefix_index = prefix.find(f"\n{VueTagConst.TS_START}")
        if prefix_index != -1:
            # logger.info(f"{prefix_index} {prefix} xxx {prefix[prefix_index:]}")
            prefix = prefix[prefix_index:]
            # 以\n为换行符号删掉第一行
            prefix = '\n'.join(prefix.strip().split('\n')[1:])
        # 查找"</script>"的位置,对suffix进行截取
        suffix_index = suffix.find(VueTagConst.TS_END)
        # 如果找到了"</script>"，则删除它及其后面的代码
        if suffix_index != -1:
            suffix = suffix[:suffix_index]
    elif (f"\n{VueTagConst.HTML_START}" in prefix or prefix.startswith(VueTagConst.HTML_START)) and (
            VueTagConst.HTML_END in suffix or not suffix.strip()):
        language = FrontLanguageEnum.HTML
        # html部分带上template标签
        prefix_index = prefix.find(VueTagConst.HTML_START)
        if prefix_index != -1:
            prefix = prefix[prefix_index:]
        suffix_index = suffix.find(VueTagConst.HTML_END)
        if suffix_index != -1:
            suffix = suffix[:suffix_index] + VueTagConst.HTML_END
    else:
        # 如果没有找到"<script>"或"<template>"，则返回原始代码块
        pass

    return language, prefix, suffix


# 清空缓存
def cache_clear():
    cache.clear()


def get_completion_cache_key(prompt):
    hash_object = hashlib.sha256()
    hash_object.update(prompt.encode('utf-8'))
    return hash_object.hexdigest()


def completion_make_cache(cache, completion_cache_time, prompt, text):
    """
    @param: prompt 预处理后的 promt
    @param: choices 请求模型返回的结果
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
        # 续期
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
    计算字符串的最长前缀后缀匹配长度
    :param content: 字符串
    :return: 匹配长度数组
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
        # 考虑最后lastTokensToConsider个字符组成的字符串的前后缀重复字符数
        max_match = max(match_lengths[:config["lastTokensToConsider"]])
        if (
            len(content) >= config["lastTokensToConsider"]
            and config["lastTokensToConsider"] - 1 - max_match <= config["maxTokenSequenceLength"]
        ):
            return True
    return False


def is_repetitive(content):
    """
    判断字符串结尾是否为重复内容
    计算规则参考https://devops.atrust.sangfor.com/demand/research_develop/3580/issues/695246
    :param content: 字符串内容
    :return: 是否为重复内容
    """
    return is_repetitive_content(content[::-1]) or \
        is_repetitive_content("".join(filter(lambda s: len(s.strip()) > 0, reversed(content))))


def contains_only_non_alpha(input_string):
    # 判断字符串是否仅包含非字母字符
    return all(not c.isalpha() for c in input_string)


def check_context_include_text(text, prefix, suffix):
    # 验证text是否是上文结尾部分，以及是否是下文开头部分或者存在下文内容行数两倍于text的内容中
    if not text.strip():
        return True
    if len(text.strip()) <= 3 and suffix.strip().startswith(text.strip()[0]):
        # 分析es数据，发现1~2+一个换行字符场景且和下文开头部分相同，则认为是上文结尾部分，且大部分场景是补全; ' );等，直接返回空
        return True
    if contains_only_non_alpha(text) and suffix.strip().startswith(text.strip()[0]):
        # 分析es数据，当text只有符号且下文以text第一个非空字符开头时，认为是上文结尾部分，且大部分场景是补全; ' );等，直接返回空
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
        # 当返回行数较少时容易误判，这里添加行数条件
        # https://devops.atrust.sangfor.com/demand/research_develop/3580/issues/815665
        return True
    else:
        return False


def cut_suffix_overlap(text, prefix, suffix, cut_suffix_line=3):
    """
    去除「补全内容」与suffix的前缀重叠部分
    :param text: 补全内容
    :param prefix: 上文
    :param suffix: 下文
    :param cut_suffix_line: 截取suffix的行数
    :return:
    """
    if not text:
        return text

    text = text.rstrip()
    text_len = len(text)
    suffix = suffix.strip()

    # 循环多次，每次都截掉suffix的首行再进行内容重叠切割（循环多次的原因是：LLM的缺陷可能会导致text与suffix较后的内容重叠）
    for _ in range(cut_suffix_line):
        new_text = text
        spilt_suffix = suffix.split("\n")
        suffix_len = len(suffix)
        if text_len == 0 or suffix_len == 0:
            return new_text

        first_line_suffix_len = len(spilt_suffix[0])
        max_overlap_length = min(text_len, suffix_len)
        for i in range(max_overlap_length, int(max_overlap_length / 2), -1):
            # 若suffix首行长度 大于 判重长度，则直接返回
            if i < first_line_suffix_len:
                break
            # 若suffix首行长度 等于 判重长度 且 首行仅有一个单词，那么无需判重直接返回
            if i == first_line_suffix_len and len(suffix[:i].split(" ")) == 1:
                break

            # 一旦text 和 suffix 存在重叠部分， 立刻返回
            if new_text[text_len - i:] == suffix[:i]:
                return new_text[:text_len - i]
        suffix = "\n".join(spilt_suffix[1:])
    return text


def cut_repetitive_text(text):
    """
    去除补全内容中的重复内容
    :param text:
    :return:
    """
    if not text:
        return text

    # 行数超过3才触发去重（该策略的前提是：若模型开始长篇大论重复，则模型产生的内容通常有很多行）
    line_count = len(text.split("\n"))
    if line_count < 3:
        return text
    return do_cur_repetitive_text(text, ratio=0.15)


def do_cur_repetitive_text(text, ratio=0.15):
    """
    若最长前后缀匹配长度占比超过阈值ratio，则去除补全内容中的重复内容
    :param text:
    :param ratio:
    :return:
    """
    if not text:
        return text

    # 计算text末尾有多少\n
    last_line_count = 0
    for i in range(len(text) - 1, -1, -1):
        if text[i] == '\n':
            last_line_count += 1
        else:
            break

    # 逆转补全文本
    text = text.rstrip()[::-1]

    # 计算当前逆转后的补全文本的最长前后缀长度
    max_match_lengths = max(max(compute_prefix_suffix_match_length(text)), 0)

    # 若 最长前后缀长度/补全内容长度 大于等于 ratio 则判断为重复内容
    if max_match_lengths > 0 and max_match_lengths / len(text) >= ratio:
        text = text[max_match_lengths + 1:]

    text = text[::-1]

    # 还原\n
    for i in range(last_line_count):
        text = text + "\n"
    return text



def get_repetitive_rate(text):
    """
    计算补全内容中的重复内容占比
    :param text:
    :return:
    """
    if not text:
        return 0

    # 逆转补全文本
    text = text.rstrip()[::-1]

    # 计算当前逆转后的补全文本的最长前后缀长度
    max_match_lengths = max(max(compute_prefix_suffix_match_length(text)), 0)

    # 计算重复内容占比
    return max_match_lengths / len(text)


def judge_css(language, text, ratio=0.7):
    """
    判断文本是否为css样式（满足多行CSS属性 or 对所有单行进行判断，假设超过70%的行是CSS属性，则认为该文本是CSS）
    :param language:
    :param text:
    :param ratio:
    :return:
    """
    if language not in FrontLanguageEnum.get_values():
        return False
    if text.count('\n') == 0:
        return False
    # 判断是否为多行CSS属性
    if re.search(multiline_css_property_pattern, text):
        return True
    count = 0
    line_count = 0
    # 判断单行是否为CSS属性(每一行进行is_css判断，假设超过70%的行是CSS属性，则认为该文本是CSS)
    for line in text.split('\n'):
        if line in ('\n', ''):
            continue
        if include_css(line):
            count += 1
        line_count += 1
    if count / line_count > ratio:
        return True
    return False


def include_css(line):
    """
    包含css样式
    :param line:
    :return:
    """
    # 去除CSS注释
    line = re.sub(css_comment_pattern, '', line)

    # 检查是否包含CSS属性
    if re.search(css_property_pattern, line):
        return True

    # 检查是否包含CSS选择器
    if re.search(css_selector_pattern, line):
        return True

    return False


def is_valid_brackets(text):
    # 用于判断text字符串中括号是否完整
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


def is_valid_content(text):
    return text.strip() != ""


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
