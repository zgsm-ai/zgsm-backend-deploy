#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 王政
# @time    : 2024/9/10 15:04
# @desc:
# -*- coding: utf-8 -*-
import hashlib
import random
import re


class StrUtil:

    @classmethod
    def random(cls, count=10):
        """
        生成随机字符串
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
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
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
        在prefix_list中找到与字符串a匹配字符最多的字符串。
        # 示例用法
        prefix_list = ["pre", "prefix", "pref", "prelude"]
        a = "prefixation"
        print(find_best_match(prefix_list, a))  # 输出: "prefix"
        :param prefix_list: 字符串列表
        :param a: 目标字符串
        :return: 与a匹配字符最多的字符串
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
        判断一个URL字符串是否是另一个带占位符的URL字符串填充后的结果。
        # 示例用法
        template_url = "/v1/namespaces/@namespaces/alarm/atemplate/@name"
        filled_url = "/v1/namespaces/default/alarm/atemplate/alarm1"
        :param template_url:
        :param filled_url:
        :return:
        """
        # 将占位符替换为正则表达式中的通配符
        pattern = re.sub(r'@[^/]+', r'[^/]+', template_url)
        # 在开始和结束添加锚点
        pattern = f'^{pattern}$'

        # 使用正则表达式匹配
        return re.match(pattern, filled_url) is not None

    @classmethod
    def remove_url_params(cls, url):
        """
        删除URL中的参数部分，但保留方法参数
        print(remove_url_params("http://example.com/path?param1=value1&param2=value2"))
        输出: http://example.com/path
        print(remove_url_params("http://example.com/path?_method=get&param1=value1"))
        输出: http://example.com/path?_method=delete
        print(remove_url_params("http://example.com/path?_method=delete"))
        输出: http://example.com/path?_method=delete
        print(remove_url_params("http://example.com/path"))
        输出: http://example.com/path
        :param url:
        :return:
        """
        match = re.search(r'(\?_method=[^&]*)(?:&|$)|\?.*', url)
        if match:
            # 如果匹配到_method参数，保留它
            if match.group(1):
                return url[:match.start()] + match.group(1)
            else:
                return url[:match.start()]
        return url
