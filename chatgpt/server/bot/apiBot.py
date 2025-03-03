#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A simple wrapper for the official ChatGPT API

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 陈烜 42766
    :更新时间: 2023/3/24 14:12
"""
import os
import re
from typing import List

import openai
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from tenacity import RetryError

from bot.bot_util import compute_tokens
from bot.chat_history import ChatHistory, get_history
from bot.prompt import Prompt
from common.constant import GPTModelConstant, PromptConstant, AskStreamConfig, \
    ActionsConstant, GPTConstant, ScribeConstant, ConfigurationConstant
from common.exception.exceptions import OpenAiRequestError, OperationError, RequestError
from common.utils.util import random_completion_id, remove_duplicate_string, check_and_set_key_path
from services.system.configuration_service import ConfigurationService
from third_platform.es.chat_messages.prompt_es_service import prompt_es_service
from third_platform.es.chat_messages.chatbot_es_service import chatbot_es
from config import conf, CONFIG
import logging
import time
from datetime import datetime

ENGINE = os.environ.get("GPT_ENGINE") or "text-davinci-003"


def get_content(completion, stream=False):
    if stream:
        return completion["choices"][0]["delta"].get("content", None)
    else:
        return completion["choices"][0]["message"].get("content", None)


def get_finish_reason(response):
    """
    完成原因。每个回复都包含 finish_reason。 finish_reason 可能的值为：
        stop：API 返回了完整的模型输出。
        length：由于 max_tokens 参数或标记限制，模型输出不完整。
        content_filter：由于内容筛选器的标志，省略了内容。
        null：API 回复仍在进行中或未完成。
    """
    return response["choices"][0]["finish_reason"]


def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4000 - compute_tokens(prompt)


class ChatPocket:
    """
    聊天信息夹袋
    """
    def __init__(self,
                 model: str = '',
                 messages: list = None,
                 temperature: float = 0.5,
                 stream: bool = False,
                 request_data: dict = None
                 ):
        """
        Initialize chat arguments
        :param messages: 消息列表,包含迄今为止对话的消息列表。
        :param temperature: 介于 0 和 2 之间。较高的值（如 0.8）将使输出更加随机，而较低的值（如 0.2）将使其更加集中和确定性。
        :param stream: 是否流式传输
        :param max_tokens: 最大token，聊天完成时生成的最大令牌数。输入标记和生成标记的总长度受到模型上下文长度的限制
        :param seed: 随机种子，整数或者空值，如果指定，我们的系统将尽最大努力进行确定性采样，以便具有相同seed参数的重复请求应返回相同的结果。
                     不保证确定性。
        """
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.stream = stream
        self.request_data = request_data if request_data is not None else {}
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.start_time = None
        self.first_response_time = None
        self.end_time = None
    
    def save_time(self, start_time: datetime = None,
                 first_response_time: datetime = None,
                 end_time: datetime = None):
        """
        保存对话过程的三个关键时间点
        """
        if start_time:
            self.start_time = start_time
        if first_response_time:
            self.first_response_time = first_response_time
        if end_time:
            self.end_time = end_time

    def save_tokens(self, prompt_tokens: int = 0, completion_tokens: int = 0):
        """
        保存发送给LLM的token数以及LLM输出的token数
        """
        if prompt_tokens > 0:
            self.prompt_tokens = prompt_tokens
        if completion_tokens > 0:
            self.completion_tokens = completion_tokens

    def save_completion_tokens(self, completion_tokens: int):
        """
        保存LLM返回的token数
        """
        self.completion_tokens = completion_tokens

    def get_usage(self) -> dict:
        """
        获取和chat.completion通讯消耗的token数
        """
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens
        }
    
    def to_request(self) -> dict:
        """
        转换为发送给chat.completion.create接口的数据
        """
        kwargs = {
            'model': self.model,
            'messages': self.messages,
            'temperature': self.temperature,
            'stream': self.stream,
            'seed': self.request_data.get('seed'),
            # 'extra_body': dict(username=self.request_data.get("username", "")),
        }
        response_format = self.request_data.get('response_format')
        if response_format in GPTConstant.RESPONSE_FORMAT_TYPES:
            kwargs['response_format'] = {'type': response_format}
        max_tokens = self.request_data.get('max_tokens')
        if max_tokens is not None:
            kwargs['max_tokens'] = max_tokens
        return kwargs
    
    def to_record(self) -> dict:
        """
        转换为记录到ES的数据
        """
        kwargs = self.to_request()
        req = {
            **self.request_data
        }
        # 以下三个数据在messages中已经体现，没必要再记录，这些数据可能很大，记录下来浪费空间
        req.pop("prompt")
        req.pop("code")
        req.pop("query")
        kwargs["request"] = req
        kwargs["timestamp"] = {
            "start": self.start_time,
            "first_response": self.first_response_time,
            "end": self.end_time
        }
        kwargs["usage"] = {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens
        }
        return kwargs

class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(self, 
        history: ChatHistory = None, 
        prompter: Prompt = None,
        model: str = ENGINE, 
        logger: logging.Logger = None,
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.model = self.get_req_model(model)
        self.history = history
        self.promper = prompter
        self.continue_count = 0  # 当前续写次数
        self.base_url = CONFIG.app.PEDESTAL_SERVER.get('server_url', "") + '/v1'
        self.api_key = CONFIG.app.PEDESTAL_SERVER.get('api_key', "")
        self.openai_client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

    @staticmethod
    def mock_complation(stream=False, model=None, content='回答问题', finish_reason="stop"):
        """
        在env 环境变量配置文件里面 添加 MOCconf.get('mock_complation') K_COMPLATION=True
        当 key 没有 某种模型权限的时候 构造会话数据，仅用于测试和开发环境，
        @param stream 流水传输
        @param model 模型
        @param content mock内容
        """
        created_time = int(time.time())
        if stream:
            return [ChatCompletionChunk(**{
                "choices": [
                    {
                        "delta": {
                            "content": content
                        },
                        "finish_reason": None,
                        "index": 0
                    }
                ],
                "created": created_time,
                "id": "chatcmpl-72cPkwoBZAMHoYysSNLzdUq4HGoTj",
                "model": model,
                "object": "chat.completion.chunk"
            }), ChatCompletionChunk(**{
                "choices": [
                    {
                        "delta": {},
                        "finish_reason": "stop",
                        "index": 0
                    }
                ],
                "created": created_time,
                "id": "chatcmpl-72cPkwoBZAMHoYysSNLzdUq4HGoTj",
                "model": model,
                "object": "chat.completion.chunk"
            })]
        else:
            response = ChatCompletionChunk(**PromptConstant.RESPONSE_TEMPLATE)
            response['created'] = created_time
            response['model'] = model
            response['choices'][0]['finish_reason'] = finish_reason
            response['choices'][0]['message']['content'] = content
            return response

    def _post_chat_completions(self, chat: ChatPocket):
        """
        发送对话补全请求
        """
        kwargs = chat.to_request()
        try:
            self.logger.info(f"Chatbot._post_chat_completions(): kwargs: {kwargs}")
            chat_completion = self.openai_client.chat.completions.create(**kwargs)
            return chat_completion
        except openai.APIStatusError as e:
            raise OperationError(e)
        except Exception as e:
            raise OpenAiRequestError(e)

    def _process_completion(self,
        completion: openai.ChatCompletion,
        chat: ChatPocket
    ) -> dict:
        request_data = chat.request_data
        completion = completion.model_dump()  # 转成字典
        can_continue = False
        if completion.get("choices") is None:
            raise Exception("ChatGPT API returned no choices")
        if len(completion["choices"]) == 0:
            raise Exception("ChatGPT API returned no choices")
        if get_finish_reason(completion) == 'length':
            self.logger.info("ChatGPT API returned no text, Maybe the completion is not complete, "
                         f"you can try to send 'continue' continue prompt, "
                         f"current continue count: {self.continue_count}")
            can_continue = True
        content = get_content(completion)
        if content is None:
            raise Exception("ChatGPT API returned no text")

        usage = completion.get("usage", {})
        # 本地计算和返回的prompt_tokens有点差别，这里记录本地计算的prompt_tokens与日志打印的同步
        chat.save_tokens(completion_tokens=usage.get("completion_tokens"))
        # 非流式
        if completion.get('model'):
            request_data['model'] = completion.get('model')
        prompt_es_service.insert_prompt(chat.to_record(), content, usage)
        if can_continue \
                and request_data.get('action') in GPTConstant.ALLOW_CONTINUE_ACTIONS \
                and self.continue_count < GPTConstant.MAX_CONTINUE_COUNT:
            response_text = completion['choices'][0].get('message', {}).get('content', '')
            _completion = self.continue_generate(request_data, response_text, stream=False)
            new_response_text = _completion['choices'][0].get('message', {}).get('content', '')
            all_content = response_text
            try:
                all_content = self.merge_completion_content(response_text, new_response_text)
            except Exception as e:
                self.logger.info(f'续写处理异常: {str(e)}')
            # 方法中会直接改变completion中的值
            check_and_set_key_path(completion, ['choices', 0, 'message', 'content'], all_content)
        return completion

    @staticmethod
    def merge_completion_content(response_text, new_response_text):
        """
        合并原始内容和续写的内容
        :param response_text: 原始内容
        :param new_response_text: 续写的内容
        :return: 合并后的内容
        """
        # 上次生成 行列表
        pre_last_lines = response_text.splitlines()

        def get_response_text_lines(rt):
            # 首行内容、下一行内容
            if not isinstance(rt, list):
                rt = rt.splitlines()
            if len(rt) > 2:
                one_line, two_line = rt[0], rt[1]
                rt = rt[1:]
            elif len(rt) == 1:
                one_line = rt[0]
                two_line = ""
            else:
                one_line = two_line = ""
            return one_line, two_line, rt

        first_line, second_line, new_response_text_lines = get_response_text_lines(new_response_text)
        continue_first_line = first_line  # 续写首行

        while re.search(r'```(.+)\n$', continue_first_line + '\n') \
                or continue_first_line == pre_last_lines[-2]:
            continue_first_line = second_line
            first_line, second_line, new_response_text_lines = get_response_text_lines(new_response_text_lines)

        pre_last_line = pre_last_lines[-1]
        overlap = remove_duplicate_string(pre_last_line, continue_first_line)
        new_response_text = "\n".join(new_response_text_lines)
        if continue_first_line[overlap:] == continue_first_line:
            all_content = response_text + continue_first_line[overlap:] + '\n' + new_response_text
        elif continue_first_line[overlap:] == "":
            all_content = response_text + new_response_text
        else:
            all_content = response_text + continue_first_line[overlap:] + '\n' + new_response_text
        return all_content

    def _process_completion_stream(self,
        completion: openai.Stream,
        chat: ChatPocket
    ):
        """
        处理补全请求流式返回的结果数据
        """
        request_data = chat.request_data
        full_response = ""
        completion_tokens = 1  # 下面生成器少算了一个，这里由1开始，保持和不开stream的效果一样
        # 循环节记录
        hash_table = {}
        hash_tokens = {}
        loop_start = -1
        loop_length = -1
        loop_count = 1
        can_continue = False  # 是否能续写
        current_model_is_set = False
        try:
            for response in completion:
                response = response.model_dump()  # 转成字典
                if not response.get('id'):  # 第一条为空，跳过处理
                    continue
                if response.get("choices") is None:
                    raise Exception("ChatGPT API returned no choices")
                if len(response["choices"]) == 0:
                    raise Exception("ChatGPT API returned no choices")
                if response["choices"][0].get("finish_details") is not None:
                    break
                if response.get('model') and not current_model_is_set:
                    request_data['model'] = response.get('model')
                    current_model_is_set = True
                # TODO: 要考虑以下其他模型的情况
                if get_finish_reason(response) == "stop":
                    break
                if get_finish_reason(response) == 'length':
                    self.logger.info("ChatGPT API returned no text, Maybe the completion is not complete, "
                                 f"you can try to send 'continue' continue prompt, "
                                 f"current continue count: {self.continue_count}")
                    can_continue = True
                    break
                if response["choices"][0].get("delta", {}).get("role") == "assistant":
                    continue
                content = get_content(response, True)
                if content is None:
                    if completion_tokens == 1:
                        # 第一个为空说明数据全空，这里直接异常中止
                        raise Exception("ChatGPT API returned no text")
                    else:
                        # completion token不完整场景的最后一个content为空，这里仅提示异常，直接终止会导致问题历史记录保存失败，影响关联会话
                        self.logger.warning('ChatGPT API returned no content.')
                        continue
                # 判断循环节
                if content in hash_table:
                    if loop_start != -1 and content == hash_tokens[completion_tokens - loop_length]:
                        if completion_tokens + 1 - loop_start == loop_length * 2:
                            loop_count += 1
                            # loop_count循环次数限制
                            if loop_count > AskStreamConfig.LOOP_COUNT_LIMIT:
                                self.logger.warning(f"ChatGPT API returned loop_count>{AskStreamConfig.LOOP_COUNT_LIMIT}")
                                break
                            loop_start += loop_length
                        else:
                            pass
                    else:
                        loop_start = hash_table[content]
                        loop_length = completion_tokens - loop_start
                else:
                    loop_start = -1
                    loop_length = -1
                    loop_count = 0
                hash_table[content] = completion_tokens
                hash_tokens[completion_tokens] = content

                yield content
                full_response += content
                completion_tokens += 1
        except Exception as e:
            self.logger.error(f'error in _ask_stream, prompt_tokens={chat.prompt_tokens}, msg={e}')
            if not full_response:
                yield 'ChatGPT error. please retry.'
        finally:
            if completion is not None and hasattr(completion, 'close'):
                completion.close()
        if full_response:
            chat.save_time(end_time=datetime.now())
            chat.save_tokens(completion_tokens=completion_tokens)
            prompt_es_service.insert_prompt(request_data, response_content=full_response, usage=chat.get_usage())
            chatbot_es.insert_chat_completion(chat.to_record(), request_data, response_content=full_response)
        else:
            self.logger.warning(f"full_response is empty, skip add history， prompt_tokens={chat.prompt_tokens}")

        if can_continue \
                and request_data.get('action') in GPTConstant.ALLOW_CONTINUE_ACTIONS \
                and self.continue_count < GPTConstant.MAX_CONTINUE_COUNT:
            yield GPTConstant.CONTINUE_SIGN
            yield from self.continue_generate(request_data, full_response)

    def continue_generate(self, request_data, generated_text, stream=True):
        """
        续写，继续生成
        """
        self.continue_count += 1
        prompt = ConfigurationService.get_prompt_template(ConfigurationConstant.CONTINUE_PROMPT)
        last_lines = generated_text.splitlines()
        last_line = ''
        # 取已生成代码最后一行，加入续写prompt，若为空，则往上获取
        i = -1
        while last_line.strip() == '' and len(last_lines) > abs(i):
            last_line = '\n'.join(last_lines[i:])
            i -= 1
        prompt = prompt.format(lastText=last_line)
        self.logger.info(f'gpt continue. {self.continue_count}, prompt: {prompt}')
        continue_request_data = request_data.copy()
        # response_format 模式续写会出现无限循环空字符，所以去掉 response_format
        # TODO: 后续看怎么优化得更通用一点
        continue_request_data.pop('response_format', '')
        continue_request_data['action'] = ActionsConstant.CONTINUE
        continue_request_data['prompt'] = prompt
        if 'extra_kwargs' in continue_request_data:
            continue_request_data['extra_kwargs']['id'] = random_completion_id(ScribeConstant.ES_ID_TITLE)
        else:
            continue_request_data['extra_kwargs'] = {
                'id': random_completion_id(ScribeConstant.ES_ID_TITLE)
            }
        return self.ask(
            question=continue_request_data['prompt'],
            request_data=continue_request_data,
            temperature=0,
            stream=stream
        )

    def construct_messages(self, new_prompt: str, context_association: bool = True):
        """
        根据会话历史，构造消息列表messages
        """
        prompter = self.promper 
        if prompter is None:
            prompter = Prompt()
        history = self.history
        if history is not None:
            history = get_history()
        return prompter.construct_messages(history.chat_history, new_prompt, context_association)

    def ask(self,
        question: str,
        temperature: float = 0.5,
        context_association: bool = True,
        request_data: dict = None,
        stream: bool = True):
        """
        利用大模型回答用户提问
        """
        if stream:
            return self._ask_stream(question, temperature, context_association, request_data)
        else:
            return self._ask_await(question, temperature, context_association, request_data)

    def _ask_await(self,
        question: str,
        temperature: float = 0.5,
        context_association: bool = True,
        request_data: dict = None,
    ) -> dict:
        """
        Send a request to ChatGPT and return the response
        """
        try:
            before_time = int(time.time())

            # 聊天场景换 gpt3.5 的 chat 模型
            messages, prompt_tokens = self.construct_messages(question, context_association)
            chat = ChatPocket(model=self.model,
                messages=messages,
                temperature=temperature,
                stream=False,
                request_data=request_data
            )
            self.logger.info(
                f"start ask chat_completion with model={self.model},"
                f" conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")

            # 是否需要mock 会话数据
            if conf.get('mock_complation'):
                completion = self.mock_complation()
            elif messages[0]['content'] == PromptConstant.TOKENS_OVER_LENGTH:
                completion = self.mock_complation(model=self.model, content=PromptConstant.TOKENS_OVER_LENGTH)
            else:
                completion = self._post_chat_completions(chat)

            after_time = int(time.time())
            self.logger.info(f"finish ask, get completion time is {after_time - before_time}s, with model={self.model} "
                         f"conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")
            chat.save_time(start_time=before_time,end_time=after_time)
            chat.save_tokens(prompt_tokens=prompt_tokens)
            return self._process_completion(completion, chat)
        except openai.InternalServerError as e:
            self.logger.error(f"unfinish ask,with model={self.model} "
                          f"conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")
            raise OperationError(e)
        except Exception as e:
            self.logger.error(f"unfinish ask,with model={self.model} "
                          f"conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")
            raise RequestError(e)

    def _ask_stream(self,
        question: str,
        temperature: float = 0.5,
        context_association: bool = True,
        request_data: dict = None,
    ) -> str:
        """
        Send a request to ChatGPT and yield the response
        """
        try:
            before_time = datetime.now()

            # 聊天场景换 gpt3.5 的 chat 模型
            messages, prompt_tokens = self.construct_messages(question, context_association)
            chat = ChatPocket(model=self.model, 
                messages=messages,
                temperature=temperature,
                stream=True,
                request_data=request_data)
            # 是否需要mock 会话数据
            if conf.get('mock_complation'):
                completion = self.mock_complation(stream=True)
            elif messages[0]['content'] == PromptConstant.TOKENS_OVER_LENGTH:
                completion = self.mock_complation(stream=True,
                                                  model=self.model,
                                                  content=PromptConstant.TOKENS_OVER_LENGTH)
            else:
                completion = self._post_chat_completions(chat=chat)

            after_time = datetime.now()
            self.logger.info(f"Chatbot._ask_stream() finished: completion time is {after_time - before_time},"
                         f" conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")
            chat.save_tokens(prompt_tokens=prompt_tokens)
            chat.save_time(start_time=before_time, first_response_time=after_time)
            return self._process_completion_stream(completion, chat=chat)
        except RetryError:
            self.logger.error(f"Chatbot._ask_stream() unfinish: with model={self.model} "
                          f"conversation_id={request_data.get('conversation_id')}, prompt_tokens={prompt_tokens}")
            raise OpenAiRequestError()

    @staticmethod
    def get_req_model(model: str):
        if model in GPTModelConstant.GPT_35_CHAT_MODELS:
            return GPTModelConstant.GPT_35
        return model
