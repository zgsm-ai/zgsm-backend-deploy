#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: 黄鹏龙 20036
@Date  :  2024/07/24
@Desc : Completion model processing class
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
    def get_client(self, host, model, data, api_key):
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
                # Model request content exceeds the maximum time, exit
                if int((time.time() - context_and_intention.st) * 1000) >= max_model_cost_time:
                    stream_handler.mark_exception_flag()
                    break

                # Check if the completion content is empty, skip the current content
                if not chunk:
                    continue

                chunk_text = chunk.decode('utf-8')
                # Check if the completion ends normally, cancel the exception flag, exit
                if self.check_chunk_done(chunk_text):
                    stream_handler.unmark_exception_flag()
                    break

                # Check if the completion content is invalid, skip the current content
                if not self.check_chunk_content(chunk_text):
                    continue

                shell_text = json.loads(chunk_text[len(OpenAIStreamContent.CHUNK_START_WORD):])['choices'][0]['text']

                # During streaming output, exit completion under specific logic for single/multi-line scenarios
                if not stream_handler.handle(shell_text):
                    logger.info(f"Completion stream output terminated early, content is: {stream_handler.get_completed_content()}")
                    break

        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.exception(f"Completion stream terminated abnormally, exception information is: {e}")
        finally:
            choices.close()
        return stream_handler.get_completed_content_and_handle_ex()


class LocalClientStrategy(AbstractModelClientStrategy):
    def get_client(self, host, model, data, api_key):
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
                # During streaming output, exit completion under specific logic for single/multi-line scenarios
                if not stream_handler.handle(c.token.text):
                    logger.info(f"Completion stream output terminated early, content is: {stream_handler.get_completed_content()}")
                    break
        except Exception as e:
            stream_handler.mark_exception_flag()
            logger.error(f"Completion stream terminated abnormally, exception information is: {e}")
        finally:
            choices.close()
        return stream_handler.get_completed_content_and_handle_ex()
