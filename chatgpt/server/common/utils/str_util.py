#!/usr/bin/python
# -*- coding:utf-8 -*-

import hashlib
import random
import re


class StrUtil:

    @classmethod
    def random(cls, count=10):
        """
        Generate random string
        """
        return ''.join(
            random.sample(
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i',
                 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'],
                count)
        )

    @classmethod
    def is_contain_chinese(cls, string):
        """
        Check if the entire string contains Chinese characters
        :param string: The string to check
        :return: bool
        """
        if not string:
            return False
        for ch in str(string):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    @classmethod
    def generate_hash_id(cls, input_string):
        return str(hashlib.sha256(input_string.encode()).hexdigest())

    @classmethod
    def find_best_match(cls, prefix_list, text):
        """
        Find the string in prefix_list that matches the most characters in string a.
        # Example usage
        prefix_list = ["pre", "prefix", "pref", "prelude"]
        a = "prefixation"
        print(find_best_match(prefix_list, a))  # Output: "prefix"
        :param prefix_list: List of strings
        :param a: Target string
        :return: The string that matches the most characters in a
        """
        best_match = ""
        max_match_length = 0

        for prefix in prefix_list:
            if prefix not in text:
                continue
            match_length = 0
            for i in range(min(len(prefix), len(text))):
                if prefix[i] == text[i]:
                    match_length += 1
                else:
                    break

            if match_length > max_match_length:
                max_match_length = match_length
                best_match = prefix

        return best_match

    @classmethod
    def is_filled_url(cls, template_url, filled_url):
        """
        Check if a URL string is the result of filling another URL string with placeholders.
        # Example usage
        template_url = "/v1/namespaces/@namespaces/alarm/atemplate/@name"
        filled_url = "/v1/namespaces/default/alarm/atemplate/alarm1"
        :param template_url:
        :param filled_url:
        :return:
        """
        # Replace placeholders with wildcards in the regular expression
        pattern = re.sub(r'@[^/]+', r'[^/]+', template_url)
        # Add anchors at the beginning and end
        pattern = f'^{pattern}$'

        # Use regular expression to match
        return re.match(pattern, filled_url) is not None

    @classmethod
    def remove_url_params(cls, url):
        """
        Delete the parameter part of the URL, but keep the method parameters
        print(remove_url_params("http://example.com/path?param1=value1&param2=value2"))
        Output: http://example.com/path
        print(remove_url_params("http://example.com/path?_method=get&param1=value1"))
        Output: http://example.com/path?_method=delete
        print(remove_url_params("http://example.com/path?_method=delete"))
        Output: http://example.com/path?_method=delete
        print(remove_url_params("http://example.com/path"))
        Output: http://example.com/path
        :param url:
        :return:
        """
        match = re.search(r'(\?_method=[^&]*)(?:&|$)|\?.*', url)
        if match:
            # If the _method parameter is matched, keep it
            if match.group(1):
                return url[:match.start()] + match.group(1)
            else:
                return url[:match.start()]
        return url
