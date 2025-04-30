#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    """Generate random avatar background color"""
    return random.choice(UserConstant.AVATAR_COLORS)


def flatten_dept_list(dict_list, parent_name='', result=None) -> list:
    """Process multi-level department data
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
    Query string in text
    re_str: supports regex
    """
    match = re.search(re_str, text)
    return match.group() if match else None


def get_work_id_by_display_name(display_name):
    """Get work_id from username"""
    work_id_list = re.findall(r"[a-z]?\d+", display_name)
    return work_id_list[0] if work_id_list else None


def get_second_dept(dept):
    """Get second-level department"""
    return '/'.join(dept.split('/')[:2])


def timer(func):
    """Timer decorator"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} execution time: {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def code_get_line_and_language(text):
    """
    Get the total number of lines and corresponding language of markdown code blocks
    return:
        code_total_lines: Total number of lines in all code blocks
        code_languages: Languages, multiple code block languages separated by commas, use null if none
    """
    code_block_pattern = re.compile(r'```[\s\S]*?```')
    language_pattern = re.compile(r'```(\w+)')
    code_total_lines = 0
    languages = []

    for code_block in code_block_pattern.findall(text):
        # Calculate total lines in code block
        lines = len(code_block.split("\n")) - 2  # -2 because front and back ``` are also counted as lines
        code_total_lines += lines
        # Find language identifier
        language_match = language_pattern.search(code_block)
        if language_match:
            language = language_match.group(1)
        else:
            language = 'null'
        # Add language to list
        languages.append(language)

    languages = list(set(languages))  # Remove duplicates
    code_languages = ','.join(languages)
    return code_total_lines, code_languages


def random_completion_id(title):
    return f'{title}-' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(29))


def process_code_just(data):
    """
    Extract and keep only code from AI return results, set to empty if no code
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
                logger.info(f'Content without code {response_content}')
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
    """Mock streaming content"""
    for content in [content]:
        yield content


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')


def remove_duplicate_string(a, b):
    """Remove duplicate part of b in a, return start index of b after deduplication"""
    index = 0
    for i in range(1, min(len(a), len(b)) + 1):
        if a.endswith(b[:i]):
            index = i
    return index


def retry_on_exception(exception_type, retry_count=1):
    """Factory function, returns a decorator that retries a specified number of times when encountering the specified exception"""

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
                        raise RetryError(f"Still failed after {retry_count} retries, {str(e)}") from e
                    logger.info(f"Retrying... (Attempt {attempts})")

        return wrapper

    return decorator


# Function for recursively checking if a key path exists
def check_and_set_key_path(data, key_path, value_to_set=None):
    """
    Function for recursively checking if a key path exists, if value_to_set is not empty, set the value
    :param data: Data structure
    :param key_path: Path of keys, e.g., for completion['choices'][0].get('message', {}).get('content', '')
                     the key path would be key_path = ['choices', 0, 'message', 'content']
    :param value_to_set: Value to set at the specified key path, if empty only checks if path exists
    :return: If value_to_set is empty, returns boolean indicating if key path exists; otherwise returns the last level data structure
    """
    key = key_path[0]
    # If it's an int type and the data is a list
    if isinstance(key, int) and isinstance(data, list):
        if len(data) - 1 >= key:
            return check_and_set_key_path(data[key], key_path[1:], value_to_set)
        else:
            return False

    if len(key_path) == 1:  # If we've reached the last key
        if value_to_set is not None:
            data[key] = value_to_set  # Set new value
            return data
        else:
            return key in data  # Return whether the key exists
    else:
        if key not in data or data[key] is None:
            if value_to_set is not None:
                data[key] = {}  # If the path doesn't exist, create an empty dictionary
            else:
                return False  # If the path doesn't exist and no value needs to be set, return False
        return check_and_set_key_path(data[key], key_path[1:], value_to_set)


def custom_retry(min_wait=6, max_wait=20, max_attempts=5, not_exception_type=tuple()):
    """
    Custom retry decorator that supports getting retry data from function parameters,
    allowing callers to control retry logic through parameters.
    Currently used to allow callers to control the number of method retries.
    """

    def _retry_decorator(f):
        @functools.wraps(f)
        def _f_with_args(*args, **kwargs):
            # Get maximum number of attempts from function parameters
            _max_attempts = kwargs.get('retry_num')
            _max_attempts = _max_attempts if _max_attempts is not None else max_attempts
            # Create a new retry decorator using dynamic maximum attempt count
            _retry = retry(wait=wait_random_exponential(min=min_wait, max=max_wait),
                           stop=stop_after_attempt(_max_attempts),
                           retry=retry_if_not_exception_type(not_exception_type))
            # Apply the new retry decorator
            return _retry(f)(*args, **kwargs)

        return _f_with_args

    return _retry_decorator
