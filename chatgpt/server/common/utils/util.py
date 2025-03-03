#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/5/6 14:10
"""
import logging
import random
import re
import string
import time
import uuid
import functools

from common.constant import UserConstant
from common.exception.error_code import ERROR_CODE
from common.exception.exceptions import RetryError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_not_exception_type,
)  # for exponential backoff

logger = logging.getLogger(__name__)


def generate_random_avatar_color() -> str:
    """生成随机头像背景色"""
    return random.choice(UserConstant.AVATAR_COLORS)


def flatten_dept_list(dict_list, parent_name='', result=None) -> list:
    """多级部门数据处理
    return: ['a', 'a/b', 'a/b/c']
    """
    if result is None:
        result = []
    for d in dict_list:
        name = d['name']
        if parent_name:
            name = f"{parent_name}/{name}"
        result.append(name)
        if d['children']:
            flatten_dept_list(d['children'], name, result)
    return result


def re_get_string_in_text(re_str, text):
    """
    查询文本中的字符串
    re_str：支持正则
    """
    match = re.search(re_str, text)
    return match.group() if match else None


def get_work_id_by_display_name(display_name):
    """根据用户名获取 work_id"""
    work_id_list = re.findall(r"[a-z]?\d+", display_name)
    return work_id_list[0] if work_id_list else None


def get_second_dept(dept):
    """切割二级部门"""
    return '/'.join(dept.split('/')[:2])


def timer(func):
    """计时器"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 运行时间为 {end_time - start_time:.4f} 秒")
        return result

    return wrapper


def code_get_line_and_language(text):
    """
    获取markdown代码块的总行数、和对应语言
    return:
        code_total_lines: 所有代码块总行数
        code_languages: 语言，多代码块语言用,分割，没有用null表示
    """
    code_block_pattern = re.compile(r'```[\s\S]*?```')
    language_pattern = re.compile(r'```(\w+)')
    code_total_lines = 0
    languages = []

    for code_block in code_block_pattern.findall(text):
        # 计算代码块总行数
        lines = len(code_block.split("\n")) - 2  # -2是因为前后```也被计算为行
        code_total_lines += lines
        # 查找语言标识符
        language_match = language_pattern.search(code_block)
        if language_match:
            language = language_match.group(1)
        else:
            language = 'null'
        # 将语言添加到列表中
        languages.append(language)

    languages = list(set(languages))  # 去重
    code_languages = ','.join(languages)
    return code_total_lines, code_languages


def random_completion_id(title):
    return f'{title}-' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(29))


def process_code_just(data):
    """
    将ai返回结果提取只保留代码，若没代码则置空
    """
    try:
        response_content = data['choices'][0]['message']['content']
    except Exception as e:
        logger.error(e)
        response_content = None
    if response_content:
        match = re.search(r'```(.*?)\n(.*?)```', response_content, re.DOTALL)
        try:
            match_tuple = match.groups()
            if len(match_tuple) == 1:
                data['choices'][0]['message']['content'] = match_tuple[-1]
            elif len(match_tuple) == 2:
                if len(match_tuple[0]):
                    data['choices'][0]['message']['language'] = match_tuple[0]

                data['choices'][0]['message']['content'] = match_tuple[1]
            else:
                logger.info(f'有内容无代码 {response_content}')
                data['error_code'] = ERROR_CODE.SERVER.AI_RESPONSE_NO_CODE
        except Exception as e:
            logger.error(response_content)
            logger.error(e)
            data['error_code'] = ERROR_CODE.SERVER.MODEL_ERROR

    return data


def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def mock_stream_content(content=''):
    """mock 流式内容"""
    for content in [content]:
        yield content


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')


def remove_duplicate_string(a, b):
    """去除 b 在 a 中的重复部分，返回 b 去重后的开始下标"""
    index = 0
    for i in range(1, min(len(a), len(b)) + 1):
        if a.endswith(b[:i]):
            index = i
    return index


def retry_on_exception(exception_type, retry_count=1):
    """工厂函数，返回一个装饰器，该装饰器在遇到指定的异常时重试指定次数"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= retry_count:
                try:
                    return func(*args, **kwargs)
                except exception_type as e:
                    attempts += 1
                    if attempts > retry_count:
                        raise RetryError(f"重试 {retry_count} 次后仍然失败, {str(e)}") from e
                    logger.info(f"重试中...（第{attempts}次）")

        return wrapper

    return decorator


# 用于递归检查键路径是否存在的函数
def check_and_set_key_path(data, key_path, value_to_set=None):
    """
    用于递归检查键路径是否存在的函数，如果value_to_set不为空，则设置值
    :param data: 数据结构
    :param key_path: 键的路径  比如 completion['choices'][0].get('message', {}).get('content', '')
                      键的路径 就是 key_path = ['choices', 0, 'message', 'content']
    :param value_to_set: value_to_set  需要set到指定键路径的值，如果为空则只检查路径是否存在
    :return: 如果value_to_set为空，返回键路径是否存在的布尔值；否则返回最后一级的数据结构
    """
    key = key_path[0]
    # 如果是int类型并且数据是列表
    if isinstance(key, int) and isinstance(data, list):
        if len(data) - 1 >= key:
            return check_and_set_key_path(data[key], key_path[1:], value_to_set)
        else:
            return False

    if len(key_path) == 1:  # 如果到达了最后一个键
        if value_to_set is not None:
            data[key] = value_to_set  # 设置新值
            return data
        else:
            return key in data  # 返回键是否存在
    else:
        if key not in data or data[key] is None:
            if value_to_set is not None:
                data[key] = {}  # 如果路径不存在，创建一个空字典
            else:
                return False  # 如果路径不存在且不需要设置值，返回False
        return check_and_set_key_path(data[key], key_path[1:], value_to_set)


def custom_retry(min_wait=6, max_wait=20, max_attempts=5, not_exception_type=tuple()):
    """
    自定义重试装饰器，支持从函数参数获取重试的数据，调用方可以用传参来控制重试的逻辑
    当前用于调用方控制方法的重试次数
    """

    def _retry_decorator(f):
        @functools.wraps(f)
        def _f_with_args(*args, **kwargs):
            # 从函数参数中获取最大尝试次数
            _max_attempts = kwargs.get('retry_num')
            _max_attempts = _max_attempts if _max_attempts is not None else max_attempts
            # 使用动态的最大尝试次数来创建一个新的retry装饰器
            _retry = retry(wait=wait_random_exponential(min=min_wait, max=max_wait),
                           stop=stop_after_attempt(_max_attempts),
                           retry=retry_if_not_exception_type(not_exception_type))
            # 应用新的retry装饰器
            return _retry(f)(*args, **kwargs)

        return _f_with_args

    return _retry_decorator
