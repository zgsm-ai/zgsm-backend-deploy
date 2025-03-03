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
    控制流式错误响应
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
    对话机器人设置
    """
    def __init__(self, data: Dict[str, any] = None):
        """
        初始化函数，用于设置请求配置和模型参数。

        参数:
        - data (Dict[str, any]): 用户请求自带的对话机器人设置，默认为空字典。

        属性:
        - stream (bool): 是否启用流式传输，默认为 False。
        - temperature (int): 生成数据的温度参数，默认为 0。
        - model (str): 本轮对话使用的模型名称，默认为空字符串。
        - context_association (bool): 是否保留上下文，默认为 True。
        - systems (List[str]): 自定义预置系统的列表，默认为空列表。如果传入的是字符串，则自动转换为列表。
        """
        if not data:
            data = {}
        # self.raw_data = data
        # 请求配置
        self.stream: bool = data.get('stream', False)
        # 指定LLM生成数据的选项参数
        self.temperature: int = data.get('temperature', 0)
        # 本轮对话使用的模型：GPTModelConstant.GPT_TURBO
        self.model: str = data.get('model', '')
        # 是否保留上下文
        self.context_association: bool = data.get('context_association', True)
        # 自定义预置
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
        获取指定属性键对应的提示模板。

        该函数用于兼容同一Action类中存在多个提示模板的场景。如果未提供attribute_key，则默认使用self.name作为属性键。

        参数:
        - attribute_key (str): 属性键，用于指定要获取的提示模板。如果为空，则使用self.name作为默认值。

        返回:
        - str: 返回与指定属性键对应的提示模板。
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
        获取聊天机器人的角色提示词设定，返回设定的字符串列表。
        优先使用配置项设定的角色提示词设定，如果配置未设定，则使用缺省的聊天机器人角色设定
        该设定可以被各个Action改写，以实现不同的角色设定
        """
        options = options or self.get_default_options()
        return options.systems

    def get_conversation_db(self, options: ChatbotOptions = None):
        return get_redis(conf)

    def get_conversation_id(self, data: ChatRequestData):
        return data.conversation_id

    def get_history(self,  options: ChatbotOptions = None) -> ChatHistory:
        """
        获取聊天历史记录。

        参数:
        - options (ChatbotOptions, 可选): 聊天机器人的配置选项。默认为None。

        返回:
        - ChatHistory: 聊天历史记录对象。如果self.history为None，则创建一个新的ChatHistory对象。
        """
        history = self.history or ChatHistory(self.get_conversation_db(options))
        return history

    def set_history(self, history: ChatHistory) -> None:
        """
        指定使用该聊天历史记录对象。
        """
        self.history = history

    def set_logger(self, logger: logging.Logger):
        """
        指定日志输出器
        """
        self.logger = logger

    def get_prompt(self, data: ChatRequestData):
        """
        根据用户请求，获取完整的提示信息。各个Action类会加工用户请求，构造提示，以获得更高质量的模型回复
        """
        return data.prompt

    def make_chatbot(self, data: ChatRequestData = None, options: ChatbotOptions = None):
        """
        创建一个聊天机器人实例。

        参数:
        - data (ChatRequestData): 聊天请求的数据，默认为None。
        - options (ChatbotOptions): 聊天机器人的配置选项，默认为None。

        返回:
        - apiBot: 一个聊天机器人实例，包含历史记录、提示生成器和模型。

        步骤:
        1. 根据提供的选项获取模型。
        2. 根据提供的选项获取历史记录。
        3. 创建一个提示生成器，使用系统配置和模型。
        4. 返回一个包含历史记录、提示生成器和模型的聊天机器人实例。
        """
        model = self.get_model(options)
        history = self.get_history(options)
        prompter = Prompt(systems=self.get_systems(data, options), model=model)
        return apiBot(history=history, prompter=prompter, model=model, logger=self.logger)

    def ask(self, data: ChatRequestData, options: ChatbotOptions = None):
        """
        向聊天机器人发送请求并获取响应。

        参数:
        - data (ChatRequestData): 包含请求信息的ChatRequestData对象。
        - options (ChatbotOptions, 可选): 配置聊天机器人行为的选项。如果未提供，将使用默认选项。

        返回:
        - 聊天机器人的响应。如果options.stream为True，则返回流式响应；否则返回完整响应。

        流程:
        1. 如果未提供options，则使用默认选项。
        2. 根据data和options创建聊天机器人实例。
        3. 获取会话ID。
        4. 检查请求的提示信息。
        5. 记录请求的详细信息。
        6. 根据options.stream的值选择合适的请求方法（流式或非流式）。
        7. 调用聊天机器人的ask方法，并返回响应。
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
