# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/6/30 10:05
"""

import logging

import tree_sitter

from common.constant import AIReviewConstant

logger = logging.getLogger(__name__)


class TreeSitterUtil:
    parser = tree_sitter.Parser()

    @classmethod
    def load_tree_sitter(cls, language):
        return tree_sitter.Language(AIReviewConstant.TREE_SITTER_LIB_PATH, language)

    @classmethod
    def get_code_dict(cls, node):
        """
        Get the dict information of the node
        @param node: A node in the syntax tree
        @return:
        """
        code_dict = {
            'start_byte': node.start_byte,  # Index where the code block starts
            'end_byte': node.end_byte,  # Index where the code block ends
            'start_lineno': node.start_point[0] + 1,  # +1 because tree_sitter line numbers start at 0
            'end_lineno': node.end_point[0] + 1,  # Includes trailing line
            'type': node.type,
            'children': []
        }
        return code_dict

    @classmethod
    def split_code_dicts(cls, node):
        """
        Get the corresponding code segment in the source code according to the first and last lines
        @param node: Syntax tree node
        @return:
        """
        code_dicts = []
        for child_node in node.children:
            code_dict = cls.get_code_dict(child_node)
            code_dicts.append(code_dict)
            if hasattr(child_node, 'children') and len(child_node.children) > 0:
                code_dicts.extend(cls.split_code_dicts(child_node))

        return code_dicts

    @staticmethod
    def filter_codes(data, filter_type_name) -> list:
        if filter_type_name is None:
            return data

        filtered_codes = list(filter(lambda x: x['type'] in filter_type_name, data))
        return filtered_codes

    @classmethod
    def split_code(cls, language, source_code) -> list:
        """
        Cut all function codes in the code
        @param language: Programming language
        @param source_code: Source code
        @return:
        """
        language = language.lower()
        if language == "c++":
            language = "c"
        elif language == 'shell':
            language = 'bash'

        try:
            cls.parser.set_language(cls.load_tree_sitter(language.lower()))
        except Exception as e:
            logger.error(language + ' ' + str(e))
            return []
        source_code = source_code.encode('utf8')  # Chinese will cause segmentation offset, so encode it first
        tree = cls.parser.parse(source_code)

        code_dicts = cls.split_code_dicts(tree.root_node)

        filter_type_name = AIReviewConstant.TREE_SITTER_CODE_TYPE_MAP.get(language)
        filtered_codes = cls.filter_codes(code_dicts, filter_type_name)

        functions = []
        for item in filtered_codes:
            functions.append(cls.format_code_dict(item, source_code))

        return functions

    @classmethod
    def format_code_dict(cls, data, source_code) -> dict:
        # code_start = data['start_byte']
        # code_end = data['end_byte']
        # code = source_code[code_start:code_end].decode('utf8')
        lines = source_code.decode('utf-8').split('\n')
        code = lines[data['start_lineno'] - 1:data['end_lineno']]
        code = '\n'.join(code)
        code_dict = {
            'start_lineno': data['start_lineno'],
            'end_lineno': data['end_lineno'],
            'text': code
        }
        return code_dict
