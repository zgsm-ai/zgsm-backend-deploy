#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 陈烜 42766
    :更新时间: 2023/3/24 14:12
"""
import logging
import os
from datetime import date
from typing import List

from bot.bot_util import get_prompt_max_tokens, compute_tokens
from common.constant import PromptConstant


def get_default_base_prompt():
    return f"""You are a question-answering AI that can access the internet and respond in Chinese markdown format.
Current date: {str(date.today())}
"""


class Prompt:
    """
    Prompt class with methods to construct prompt
    """

    def __init__(self,
                 user: str = "User",
                 ai: str = "ChatGPT",
                 end: str = "<|im_end|>",
                 systems: List[str] = None,
                 model: str = '') -> None:
        """
        Initialize prompt with base prompt
        """
        self.username = user
        self.ainame = ai
        self.end = end
        base_prompt = os.environ.get("CUSTOM_BASE_PROMPT") or get_default_base_prompt()
        self.base_prompt = systems or [base_prompt]
        self.model = model

    @staticmethod
    def num_tokens_from_messages(messages):
        """Returns the number of tokens used by a list of messages."""
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += compute_tokens(value)
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant

        return num_tokens

    def cut_messages(self, messages):
        """
        对超大messages信息进行裁剪，保证发给接口的信息tokens数不能超过最大限制
        :param messages: 问询AI的上下文信息
        :return messages:
        """
        # Check if prompt tokens over max_token
        max_tokens = get_prompt_max_tokens(self.model)
        over_tokens = True
        max_remove = 1000
        messages_cut = False
        for _ in range(max_remove):
            if self.num_tokens_from_messages(messages) > max_tokens:
                messages_cut = True
                if len(messages) > 1:
                    messages.pop(1)
            else:
                over_tokens = False
                break
        if messages_cut:
            logging.warning("【删除历史提问】提问信息超长，自动删除部分最早的用户提问记录")
        if len(messages) <= 1:
            # 用户的提问字符串数量就超上限了，直接mock数据，后续使用
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        elif over_tokens:
            # 如果删除的信息数量超max_remove之后tokens还是超了,直接mock数据，后续使用
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        return messages

    def construct_messages(self, history_list: list, new_prompt: str, context_association: bool = True):
        """
        构造发送给LLM的消息列表

        参数:
        - history_list (list): 聊天历史列表，包含对话历史信息。
        - new_prompt (str): 用户输入的新提示信息。
        - context_association (bool): 是否关联上下文信息。默认为True。

        返回:
        - tuple: 包含两个元素的元组，第一个元素是构造好的消息列表，第二个元素是消息列表的token数量。

        功能描述:
        1. 初始化一个空的消息列表。
        2. 将基础提示信息（base_prompt）添加到消息列表中。
        3. 如果context_association为True，则将聊天历史中的上下文信息添加到消息列表中。
        4. 将用户输入的新提示信息添加到消息列表中。
        5. 调用cut_messages方法对消息列表进行裁剪。
        6. 调用num_tokens_from_messages方法计算消息列表的token数量。
        7. 返回构造好的消息列表及其token数量。

        注意:
        - 在添加上下文信息时，仅处理了用户和助手的消息，其他角色的消息可能需要进一步处理。
        """
        messages = []
        for system in self.base_prompt:
            messages.append({"role": "system", "content": system})
        if context_association:
            # 添加上下文
            for message in history_list:
                # FIXME: 可能有其他场景
                if message["role"] == self.username or message["role"] == 'user':
                    messages.append({"role": "user", "content": message['content']})
                if message['role'] == self.ainame or message["role"] == 'assistant':
                    messages.append({"role": "assistant", "content": message['content']})
        messages.append({"role": "user", "content": new_prompt})
        messages = self.cut_messages(messages)
        prompt_tokens = self.num_tokens_from_messages(messages)
        return messages, prompt_tokens

    def get_user_req_messages(self, new_prompt: str):
        messages = []
        for system in self.base_prompt:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": new_prompt})
        return messages

