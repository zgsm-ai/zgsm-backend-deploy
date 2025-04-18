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
    Control the streaming error response
    """

    def wrapper(*args, **kwargs):
        self_ = args[0]  # 类实例
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
        Initialization function for setting request configurations and model parameters.

        Parameters:
        - data (Dict[str, any]): Chatbot settings that come with the user request, default is an empty dictionary.

        Attributes:
        - stream (bool): Whether to enable streaming transmission, default is False.
        - temperature (int): Temperature parameter for generating data, default is 0.
        - model (str): The name of the model used in this round of conversation, default is an empty string.
        - context_association (bool): Whether to keep the context, default is True.
        - systems (List[str]): A list of custom preset systems, default is an empty list. If a string is passed, it will be automatically converted to a list.
        """
        if not data:
            data = {}
        # self.raw_data = data
        # Request configuration
        self.stream: bool = data.get('stream', False)
        # Specifies the option parameters for LLM to generate data
        self.temperature: int = data.get('temperature', 0)
        # Model used in this round of conversation: GPTModelConstant.GPT_TURBO
        self.model: str = data.get('model', '')
        # Whether to retain context
        self.context_association: bool = data.get('context_association', True)
        # Custom preset
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

        This function is used to be compatible with scenarios where there are multiple prompt templates in the same Action class. If attribute_key is not provided, self.name is used as the attribute key by default.

        Parameters:
        - attribute_key (str): Attribute key, used to specify the prompt template to be obtained. If empty, self.name is used as the default value.

        Returns:
        - str: Returns the prompt template corresponding to the specified attribute key.
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
        Get the role prompt settings of the chatbot and return a list of strings of the settings.
        The role prompt setting set by the configuration item is preferred. If the configuration is not set, the default chatbot role setting is used.
        This setting can be rewritten by each Action to achieve different role settings.
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
        - options (ChatbotOptions, optional): Configuration options for the chatbot. Defaults to None.

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
        Specify the log output
        """
        self.logger = logger

    def get_prompt(self, data: ChatRequestData):
        """
        Get complete prompt information according to user requests. Each Action class will process user requests and construct prompts to obtain higher-quality model replies.
        """
        return data.prompt

    def make_chatbot(self, data: ChatRequestData = None, options: ChatbotOptions = None):
        """
        Create a chatbot instance.

        Parameters:
        - data (ChatRequestData): Chat request data, default is None.
        - options (ChatbotOptions): Chatbot configuration options, default is None.

        Returns:
        - apiBot: A chatbot instance containing history, prompt generator, and model.

        Steps:
        1. Get the model according to the provided options.
        2. Get the history according to the provided options.
        3. Create a prompt generator using system configuration and model.
        4. Return a chatbot instance containing history, prompt generator, and model.
        """
        model = self.get_model(options)
        history = self.get_history(options)
        prompter = Prompt(systems=self.get_systems(data, options), model=model)
        return apiBot(history=history, prompter=prompter, model=model, logger=self.logger)

    def ask(self, data: ChatRequestData, options: ChatbotOptions = None):
        """
        Sends a request to the chatbot and retrieves the response.

        Parameters:
        - data (ChatRequestData): ChatRequestData object containing request information.
        - options (ChatbotOptions, optional): Options to configure the behavior of the chatbot. If not provided, default options will be used.

        Returns:
        - The response from the chatbot. Returns a streaming response if options.stream is True; otherwise, returns a complete response.

        Process:
        1. If options are not provided, default options are used.
        2. Create a chatbot instance based on data and options.
        3. Get the session ID.
        4. Check the prompt information of the request.
        5. Record the details of the request.
        6. Select the appropriate request method (streaming or non-streaming) based on the value of options.stream.
        7. Call the chatbot's ask method and return the response.
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
        Generate chat results

        Parameters:
        - data (ChatRequestData): Chat request data
        - options (ChatbotOptions, optional): Chatbot options, default is None

        Returns:
        - Returns the chat results generated by the `ask` method
        """
        return self.ask(data, options=options)


def process_code_retract(request_data, code):
    if not code:
        return code
    try:
        source_first_line = next((v for v in request_data.code.splitlines() if v.strip()), '')  # The first non-empty line of the input code
        if '\t' in source_first_line:
            return code  # If the input code contains tabs, no indentation processing is done
        source_strip_count = len(source_first_line) - len(source_first_line.lstrip())  # Number of spaces
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
        logging.error('Indentation processing exception', e)
    return code


# Process return code indentation
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
            logging.error('Indentation processing exception', e)
        return res

    return inner
