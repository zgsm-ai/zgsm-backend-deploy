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
    """Generate a random avatar background color"""
    return random.choice(UserConstant.AVATAR_COLORS)


def flatten_dept_list(dict_list, parent_name='', result=None) -> list:
    """Multi-level department data processing
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
    Query the string in the text
    re_str: supports regular expressions
    """
    match = re.search(re_str, text)
    return match.group() if match else None


def get_work_id_by_display_name(display_name):
    """Get work_id by username"""
    work_id_list = re.findall(r"[a-z]?\d+", display_name)
    return work_id_list[0] if work_id_list else None


def get_second_dept(dept):
    """Cut the second-level department"""
    return '/'.join(dept.split('/')[:2])


def timer(func):
    """Timer"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} running time is {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def code_get_line_and_language(text):
    """
    Get the total number of lines and corresponding language of the markdown code block
    return:
        code_total_lines: total number of lines of all code blocks
        code_languages: Language, multiple code block languages are separated by commas, and null is used if there is no language
    """
    code_block_pattern = re.compile(r'```[\s\S]*?```')
    language_pattern = re.compile(r'```(\w+)')
    code_total_lines = 0
    languages = []

    for code_block in code_block_pattern.findall(text):
        # Calculate the total number of lines in the code block
        # -2 because the before and after ``` are also counted as lines
        lines = len(code_block.split("\n")) - 2
        code_total_lines += lines
        # Find the language identifier
        language_match = language_pattern.search(code_block)
        if language_match:
            language = language_match.group(1)
        else:
            language = 'null'
        # Add the language to the list
        languages.append(language)

    languages = list(set(languages))  # Deduplication
    code_languages = ','.join(languages)
    return code_total_lines, code_languages


def random_completion_id(title):
    return f'{title}-' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(29))


def process_code_just(data):
    """
    Extract and retain only the code from the AI ​​return result, and set it to empty if there is no code
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
                logger.info(f'There is content but no code {response_content}')
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
    """mock streaming content"""
    for content in [content]:
        yield content


def generate_uuid():
    return str(uuid.uuid4()).replace('-', '')


def remove_duplicate_string(a, b):
    """Remove the duplicate part of b in a and return the starting subscript of b after deduplication"""
    index = 0
    for i in range(1, min(len(a), len(b)) + 1):
        if a.endswith(b[:i]):
            index = i
    return index


def retry_on_exception(exception_type, retry_count=1):
    """Factory function that returns a decorator that retries a specified number of times when a specified exception is encountered"""

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
                        raise RetryError(f"Failed after retrying {retry_count} times, {str(e)}") from e
                    logger.info(f"Retrying... (attempt {attempts})")

        return wrapper

    return decorator


# Function to recursively check if a key path exists
def check_and_set_key_path(data, key_path, value_to_set=None):
    """
    Function to recursively check if a key path exists, and set the value if value_to_set is not empty
    :param data: data structure
    :param key_path: key path, e.g. completion['choices'][0].get('message', {}).get('content', '')
                      The key path is key_path = ['choices', 0, 'message', 'content']
    :param value_to_set: value_to_set The value to be set to the specified key path. If it is empty, only check whether the path exists
    :return: If value_to_set is empty, return a boolean value indicating whether the key path exists; otherwise, return the last-level data structure
    """
    key = key_path[0]
    # If it is an int type and the data is a list
    if isinstance(key, int) and isinstance(data, list):
        if len(data) - 1 >= key:
            return check_and_set_key_path(data[key], key_path[1:], value_to_set)
        else:
            return False

    if len(key_path) == 1:  # If the last key is reached
        if value_to_set is not None:
            data[key] = value_to_set  # set new value
            return data
        else:
            return key in data  # Returns whether the key exists
    else:
        if key not in data or data[key] is None:
            if value_to_set is not None:
                data[key] = {}  # If the path does not exist, create an empty dictionary
            else:
                return False  # Return False if the path does not exist and no value needs to be set
        return check_and_set_key_path(data[key], key_path[1:], value_to_set)


def custom_retry(min_wait=6, max_wait=20, max_attempts=5, not_exception_type=tuple()):
    """
    Custom retry decorator, supports obtaining retry data from function parameters, and the caller can use parameters to control the retry logic
    Currently used by the caller to control the number of retries of the method
    """

    def _retry_decorator(f):
        @functools.wraps(f)
        def _f_with_args(*args, **kwargs):
            # Get the maximum number of attempts from the function parameters
            _max_attempts = kwargs.get('retry_num')
            _max_attempts = kwargs.get('retry_num')
            _max_attempts = _max_attempts if _max_attempts is not None else max_attempts
            # Use the dynamic maximum number of attempts to create a new retry decorator
            _retry = retry(wait=wait_random_exponential(min=min_wait, max=max_wait),
                           stop=stop_after_attempt(_max_attempts),
                           retry=retry_if_not_exception_type(not_exception_type))
            # Apply the new retry decorator
            return _retry(f)(*args, **kwargs)

        return _f_with_args

    return _retry_decorator
