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
        Cut oversized messages information to ensure that the number of tokens sent to the interface does not exceed the maximum limit
        :param messages: Contextual information for questioning AI
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
            logging.warning("【Delete Historical Questions】The question information is too long, automatically delete some of the earliest user question records")
        if len(messages) <= 1:
            # The number of user's question strings exceeds the limit, directly mock the data for subsequent use
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        elif over_tokens:
            # If the number of deleted information exceeds max_remove and the tokens still exceed, directly mock the data for subsequent use
            messages = [{"role": "assistant", "content": PromptConstant.TOKENS_OVER_LENGTH}]
        return messages

    def construct_messages(self, history_list: list, new_prompt: str, context_association: bool = True):
        """
        Construct a message list to send to the LLM

        Parameters:
        - history_list (list): Chat history list containing chat history information.
        - new_prompt (str): New prompt information entered by the user.
        - context_association (bool): Whether to associate context information. The default is True.

        Returns:
        - tuple: A tuple containing two elements, the first element is the constructed message list, and the second element is the number of tokens in the message list.

        Function description:
        1. Initialize an empty message list.
        2. Add basic prompt information (base_prompt) to the message list.
        3. If context_association is True, add the context information in the chat history to the message list.
        4. Add the new prompt information entered by the user to the message list.
        5. Call the cut_messages method to crop the message list.
        6. Call the num_tokens_from_messages method to calculate the number of tokens in the message list.
        7. Returns the constructed message list and the number of tokens.

        Note:
        - When adding context information, only user and assistant messages are processed, and messages from other roles may need to be further processed.
        """
        messages = []
        for system in self.base_prompt:
            messages.append({"role": "system", "content": system})
        if context_association:
            # Add context
            for message in history_list:
                # FIXME: Possible other scenarios
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
