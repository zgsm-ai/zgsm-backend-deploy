#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 黄鹏龙 20036
@Date  :  2024/07/24
@Desc : 补全模型处理类
"""

import time
import json

from abc import ABC, abstractmethod
from thrid_platform.openai_server.api_manager import OpenAiServerManager
from utils.constant import OpenAIStreamContent
from config.log_config import logger
from text_generation import Client
from services.completion_stream_service import StreamHandlerFactory


class AbstractModelClientStrategy(ABC):
    @abstractmethod
    def get_client(self, host, model, data):
        raise NotImplementedError

    @abstractmethod
    def choices_process(self, choices, context_and_intention, max_model_cost_time):
        raise NotImplementedError

    @classmethod
    def handle_host(cls, host):
        return f'http://{host}' if 'http' not in host else host

    @classmethod
    def check_chunk_content(cls, chunk_msg) -> bool:
        return (chunk_msg.startswith(OpenAIStreamContent.CHUNK_START_WORD)
                and not chunk_msg[len(OpenAIStreamContent.CHUNK_START_WORD):]
                .strip().startswith(OpenAIStreamContent.CHUNK_DONE_SIGNAL))

    @classmethod
    def check_chunk_done(cls, chunk_msg) -> bool:
        return (chunk_msg[len(OpenAIStreamContent.CHUNK_START_WORD):]
                .strip().startswith(OpenAIStreamContent.CHUNK_DONE_SIGNAL))


class ModelClientStrategy:
    def __init__(self, strategy: AbstractModelClientStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: AbstractModelClientStrategy):
        self._strategy = strategy

    def get_client(self, host, model, data, api_key):
        return self._strategy.get_client(host, model, data, api_key)

    def choices_process(self, choices, context_and_intention, max_model_cost_time):
        return self._strategy.choices_process(choices, context_and_intention, max_model_cost_time)


class OpenAIClientStrategy(AbstractModelClientStrategy):
    def get_client(self, host, model, data, api_key):
        return OpenAiServerManager(url=self.handle_host(host), model=model, api_key=api_key)

    def choices_process(self, choices, context_and_intention, max_model_cost_time):

        if choices is None:
            return ''

        stream_handler = StreamHandlerFactory.get_stream_handler(context=context_and_intention)
        try:
            for chunk in choices.iter_lines():
                # 模型请求内容超过最大时间，退出
                if int((time.time() - context_and_intention.st) * 1000) >= max_model_cost_time:
                    stream_handler.mark_exception_flag()
                    break

                # 检查到补全内容为空，跳过当前内容
                if not chunk:
                    continue

                chunk_text = chunk.decode('utf-8')
                # 检查到补全正常结束，取消设置异常标记，退出
                if self.check_chunk_done(chunk_text):
                    stream_handler.unmark_exception_flag()
                    break

                # 检查到补全内容无效，跳过当前内容
                if not self.check_chunk_content(chunk_text):
                    continue

                shell_text = json.loads(chunk_text[len(OpenAIStreamContent.CHUNK_START_WORD):])['choices'][0]['text']

                # 流式输出过程中，针对单行/多行场景满足特定逻辑下退出补全
                if not stream_handler.handle(shell_text):
                    logger.info(f"补全流式输出提前终止，内容为: {stream_handler.get_completed_content()}")
                    break

        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.exception(f"补全流式异常终止，异常信息为: {e}")
        finally:
            choices.close()
        return stream_handler.get_completed_content_and_handle_ex()


class LocalClientStrategy(AbstractModelClientStrategy):
    def get_client(self, host, model, data):
        return Client(base_url=self.handle_host(host), headers={'x-complete-id': data['x-complete-id']})

    def choices_process(self, choices, context_and_intention, max_model_cost_time):
        if choices is None:
            return ''
        stream_handler = StreamHandlerFactory.get_stream_handler(context=context_and_intention)
        try:
            for c in choices:
                if int((time.time() - context_and_intention.st) * 1000) >= max_model_cost_time:
                    stream_handler.mark_exception_flag()
                    break
                # 流式输出过程中，针对单行/多行场景满足特定逻辑下退出补全
                if not stream_handler.handle(c.token.text):
                    logger.info(f"补全流式输出提前终止，内容为: {stream_handler.get_completed_content()}")
                    break
        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.error(f"补全流式异常终止，异常信息为: {e}")
        finally:
            choices.close()
        return stream_handler.get_completed_content_and_handle_ex()
