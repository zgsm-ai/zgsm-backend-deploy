#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import json

from common.utils.util import mock_stream_content
from config import conf
from bot.apiBot import Chatbot as apiBot
from bot.prompt import Prompt
from bot.cache import get_redis
from bot.chat_history import ChatHistory
from typing import Dict, List
from services.agents.agent_data_classes import ChatRequestData

from services.system.configuration_service import ConfigurationService

def stream_error_response(func):
    """
    Handle streaming error responses
    """

    def wrapper(*args, **kwargs):
        self_ = args[0]  # class instance
        stream = args[2].stream
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if stream:
                self_.mock_stream = True
                self_.resp_headers['mock_stream'] = 1
                return mock_stream_content(str(e))
            raise e

    return wrapper

class ChatbotOptions:
    """
    Chatbot settings
    """
    def __init__(self, data: Dict[str, any] = None):
        """
        Initialization function for setting request configuration and model parameters.

        Parameters:
        - data (Dict[str, any]): User-provided chatbot settings with the request, default is an empty dictionary.

        Attributes:
        - stream (bool): Whether to enable streaming, default is False.
        - temperature (int): Temperature parameter for data generation, default is 0.
        - model (str): Model name used for this conversation round, default is an empty string.
        - context_association (bool): Whether to retain context, default is True.
        - systems (List[str]): List of custom preset systems, default is an empty list. If a string is passed, it will be automatically converted to a list.
        """
        if not data:
            data = {}
        # self.raw_data = data
        # Request configuration
        self.stream: bool = data.get('stream', False)
        # Specify LLM data generation option parameters
        self.temperature: int = data.get('temperature', 0)
        # Model used for this conversation round: GPTModelConstant.GPT_TURBO
        self.model: str = data.get('model', '')
        # Whether to retain context
        self.context_association: bool = data.get('context_association', True)
        # Custom presets
        systems = data.get("systems", list())
        if isinstance(systems, str):
            systems = [systems]
        self.systems: List[str] = systems

class ActionStrategy:
    name = "base"
    history = None
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.resp_headers = {}

    @staticmethod
    def format_prompt_string(string):
        return '{{' + str(string) + '}}'

    def get_prompt_template(self, attribute_key: str = '') -> str:
        """
        Get the prompt template corresponding to the specified attribute key.

        This function is used to support scenarios where multiple prompt templates exist within the same Action class. If attribute_key is not provided, self.name is used as the default.

        Parameters:
        - attribute_key (str): The attribute key used to specify which prompt template to get. If empty, self.name is used as the default.

        Returns:
        - str: The prompt template corresponding to the specified attribute key.
        """
        attribute_key = attribute_key if attribute_key else self.name
        prompt_template = ConfigurationService.get_prompt_template(attribute_key=attribute_key)
        return prompt_template

    @staticmethod
    def check_prompt(prompt):
        pass

    @staticmethod
    def get_default_options():
        return ChatbotOptions()

    def get_model(self, options: ChatbotOptions = None):
        return options.model or ConfigurationService.get_model_ide_normal(self.name)

    def get_api_key(self, options: ChatbotOptions = None):
        return conf.get("openai_api_key")

    def get_systems(self, data: ChatRequestData = None, options: ChatbotOptions = None):
        """
        Get the chatbot's role prompt settings, returning a list of setting strings.
        Priority is given to role prompt settings in the configuration, if not set in the configuration, use the default chatbot role settings.
        This setting can be overwritten by each Action to implement different role settings.
        """
        options = options or self.get_default_options()
        return options.systems

    def get_conversation_db(self, options: ChatbotOptions = None):
        return get_redis(conf)

    def get_conversation_id(self, data: ChatRequestData):
        return data.conversation_id

    def get_history(self,  options: ChatbotOptions = None) -> ChatHistory:
        """
        Get chat history.

        Parameters:
        - options (ChatbotOptions, optional): Chatbot configuration options. Default is None.

        Returns:
        - ChatHistory: Chat history object. If self.history is None, a new ChatHistory object is created.
        """
        history = self.history or ChatHistory(self.get_conversation_db(options))
        return history

    def set_history(self, history: ChatHistory) -> None:
        """
        Specify to use this chat history object.
        """
        self.history = history

    def set_logger(self, logger: logging.Logger):
        """
        Specify the logger
        """
        self.logger = logger

    def get_prompt(self, data: ChatRequestData):
        """
        Based on user request, get the complete prompt information. Each Action class processes user requests and constructs prompts to obtain higher quality model responses.
        """
        return data.prompt

    def make_chatbot(self, data: ChatRequestData = None, options: ChatbotOptions = None):
        """
        Create a chatbot instance.

        Parameters:
        - data (ChatRequestData): Chat request data, default is None.
        - options (ChatbotOptions): Chatbot configuration options, default is None.

        Returns:
        - apiBot: A chatbot instance that includes history, prompt generator, and model.

        Steps:
        1. Get the model based on the provided options.
        2. Get the history based on the provided options.
        3. Create a prompt generator using system configuration and model.
        4. Return a chatbot instance that includes history, prompt generator, and model.
        """
        model = self.get_model(options)
        history = self.get_history(options)
        prompter = Prompt(systems=self.get_systems(data, options), model=model)
        return apiBot(history=history, prompter=prompter, model=model, logger=self.logger)

    def ask(self, data: ChatRequestData, options: ChatbotOptions = None):
        """
        Send a request to the chatbot and get a response.

        Parameters:
        - data (ChatRequestData): ChatRequestData object containing request information.
        - options (ChatbotOptions, optional): Options to configure chatbot behavior. If not provided, default options will be used.

        Returns:
        - The chatbot's response. If options.stream is True, returns a streaming response; otherwise, returns a complete response.

        Flow:
        1. If options is not provided, use default options.
        2. Create a chatbot instance based on data and options.
        3. Get the conversation ID.
        4. Check the requested prompt information.
        5. Log the details of the request.
        6. Choose the appropriate request method (streaming or non-streaming) based on options.stream.
        """
        options = options or self.get_default_options()
        chatbot = self.make_chatbot(data, options)

        self.check_prompt(data.prompt)
        self.logger.info(f"ActionStrategy.ask(): prompt: {data.prompt}")
        self.logger.info(f"ActionStrategy.ask(): options: {options.__dict__}")
        return chatbot.ask(data.prompt,
                    temperature=options.temperature,
                    context_association=options.context_association,
                    request_data=data.to_dict(),
                    stream=options.stream)

    def make_result(self, data: ChatRequestData, options: ChatbotOptions = None):
        """
        生成聊天结果

        参数:
        - data (ChatRequestData): 聊天请求的数据
        - options (ChatbotOptions, 可选): 聊天机器人的选项，默认为None

        返回:
        - 返回通过`ask`方法生成的聊天结果
        """
        return self.ask(data, options=options)


def process_code_retract(request_data, code):
    if not code:
        return code
    try:
        source_first_line = next((v for v in request_data.code.splitlines() if v.strip()), '')  # 输入代码非空首行
        if '\t' in source_first_line:
            return code  # 输入代码含制表符，不做缩进处理
        source_strip_count = len(source_first_line) - len(source_first_line.lstrip())  # 空格数
        first_line = next((v for v in code.splitlines() if v.strip()), '')
        res_strip_count = len(first_line) - len(first_line.lstrip())
        offset = source_strip_count - res_strip_count
        new_code = None
        if offset > 0:
            new_code = '\n'.join(list(map(lambda line: ' ' * offset + line, code.splitlines())))
        elif offset < 0:
            new_code = '\n'.join(list(
                map(lambda line: line[-offset:] if line.startswith(' ' * -offset) else line,
                    code.splitlines())))

        if new_code is not None:
            if code.endswith('\n') and not new_code.endswith('\n'):
                new_code += '\n'
            return new_code
    except Exception as e:
        logging.error('缩进处理异常', e)
    return code


# 处理返回代码缩进
def process_retract(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        try:
            response_content = res['choices'][0]['message']['content']
            data = args[1]
            if data.code and response_content:
                match = re.search(r'```(.*?)\n(.*?)```', response_content, re.DOTALL)
                match_tuple = match.groups()
                if len(match_tuple) == 2:
                    code = match_tuple[1]
                    new_code = process_code_retract(data, code)
                    if new_code != code:
                        if code.endswith('\n') and not new_code.endswith('\n'):
                            new_code += '\n'
                        res['choices'][0]['message']['content'] = response_content.replace(code, new_code)
        except Exception as e:
            logging.error('缩进处理异常', e)
        return res

    return inner
