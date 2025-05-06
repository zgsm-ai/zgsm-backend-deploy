#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    Prompt class, provides methods for constructing prompts
    """

    def __init__(self,
                 user: str = "User",
                 ai: str = "ChatGPT",
                 end: str = "<|im_end|>",
                 systems: List[str] = None,
                 model: str = '') -> None:
        """
        Initialize with base prompts
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
            num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n format
            for key, value in message.items():
                num_tokens += compute_tokens(value)
                if key == "name":  # If there's a name, the role is omitted
                    num_tokens += -1  # Role is always required and always 1 token
        num_tokens += 2  # Every reply is primed with <im_start>assistant

        return num_tokens

    def cut_messages(self, messages):
        """
        Trim oversized messages to ensure tokens sent to the API do not exceed the maximum limit
        :param messages: Context information for querying AI
        :return messages:
        """
        # Check if prompt tokens exceed the maximum limit
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
            logging.warning("[Deleting Historical Questions] Question information is too long, automatically deleting some of the earliest user question records")
        if len(messages) <= 1:
            # The user's question string exceeds the limit, directly mock data for later use
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        elif over_tokens:
            # If token count still exceeds after deleting more than max_remove messages, directly mock data for later use
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        return messages

    def construct_messages(self, history_list: list, new_prompt: str, context_association: bool = True):
        """
        Construct message list to send to LLM

        Parameters:
        - history_list (list): Chat history list containing dialogue history information.
        - new_prompt (str): New prompt information input by the user.
        - context_association (bool): Whether to associate context information. Default is True.

        Returns:
        - tuple: A tuple containing two elements, the first is the constructed message list, and the second is the token count of the message list.

        Function description:
        1. Initialize an empty message list.
        2. Add base prompt information (base_prompt) to the message list.
        3. If context_association is True, add context information from chat history to the message list.
        4. Add the new prompt information input by the user to the message list.
        5. Call the cut_messages method to trim the message list.
        6. Call the num_tokens_from_messages method to calculate the token count of the message list.
        7. Return the constructed message list and its token count.

        Note:
        - When adding context information, only user and assistant messages are processed, other role messages may need further handling.
        """
        messages = []
        for system in self.base_prompt:
            messages.append({"role": "system", "content": system})
        if context_association:
            # Add context
            for message in history_list:
                # FIXME: There may be other scenarios
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

