#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A simple wrapper for the official ChatGPT API

    :Author: Chen Xuan 42766
    :Time: 2023/3/24 14:12
    :Modifier: Chen Xuan 42766
    :UpdateTime: 2023/3/24 14:12
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
    Completion reason. Each response contains finish_reason. Possible values for finish_reason are:
        stop: The API returned the complete model output.
        length: The model output is incomplete due to the max_tokens parameter or token limit.
        content_filter: Content was omitted due to a flag from the content filter.
        null: The API response is still in progress or incomplete.
    """
    return response["choices"][0]["finish_reason"]


def get_max_tokens(prompt: str) -> int:
    """
    Get the max tokens for a prompt
    """
    return 4000 - compute_tokens(prompt)


class ChatPocket:
    """
    Chat information pocket
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
        :param messages: Message list, containing the list of messages for the conversation so far.
        :param temperature: Between 0 and 2. Higher values (such as 0.8) will make the output more random, while lower values (such as 0.2) will make it more focused and deterministic.
        :param stream: Whether to stream
        :param max_tokens: Maximum token, the maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length
        :param seed: Random seed, integer or null value, if specified, our system will make the best effort to sample deterministically, so that repeated requests with the same seed parameter should return the same result.
                     Determinism is not guaranteed.
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
        Save the three key time points of the conversation process
        """
        if start_time:
            self.start_time = start_time
        if first_response_time:
            self.first_response_time = first_response_time
        if end_time:
            self.end_time = end_time

    def save_tokens(self, prompt_tokens: int = 0, completion_tokens: int = 0):
        """
        Save the number of tokens sent to LLM and the number of tokens output by LLM
        """
        if prompt_tokens > 0:
            self.prompt_tokens = prompt_tokens
        if completion_tokens > 0:
            self.completion_tokens = completion_tokens

    def save_completion_tokens(self, completion_tokens: int):
        """
        Save the number of tokens returned by LLM
        """
        self.completion_tokens = completion_tokens

    def get_usage(self) -> dict:
        """
        Get the number of tokens consumed by chat.completion communication
        """
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens
        }
    
    def to_request(self) -> dict:
        """
        Convert to data sent to the chat.completion.create interface
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
        Convert to data recorded in ES
        """
        kwargs = self.to_request()
        req = {
            **self.request_data
        }
        # The following three data are already reflected in messages, there is no need to record them again, these data may be very large, recording them will waste space
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
        self.continue_count = 0  # Current number of continuation attempts
        self.base_url = CONFIG.app.PEDESTAL_SERVER.get('server_url', "") + '/v1'
        self.api_key = CONFIG.app.PEDESTAL_SERVER.get('api_key', "")
        self.openai_client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

    @staticmethod
    def mock_complation(stream=False, model=None, content='Answer the question', finish_reason="stop"):
        """
        Add MOCconf.get('mock_complation') K_COMPLATION=True in the env environment variable configuration file
        When the key does not have permission for a certain model, construct conversation data, only for testing and development environments,
        @param stream Streaming transmission
        @param model Model
        @param content Mock content
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
        Send dialogue completion request
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
        completion = completion.model_dump()  # Convert to dictionary
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
        # The local calculation and the returned prompt_tokens are a bit different, here record the locally calculated prompt_tokens to synchronize with the log printing
        chat.save_tokens(completion_tokens=usage.get("completion_tokens"))
        # Non-streaming
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
                self.logger.info(f'Continuation processing exception: {str(e)}')
            # The method will directly change the values in completion
            check_and_set_key_path(completion, ['choices', 0, 'message', 'content'], all_content)
        return completion

    @staticmethod
    def merge_completion_content(response_text, new_response_text):
        """
        Merge the original content and the continued content
        :param response_text: Original content
        :param new_response_text: Continued content
        :return: Merged content
        """
        # Last generated line list
        pre_last_lines = response_text.splitlines()

        def get_response_text_lines(rt):
            # First line content, next line content
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
        continue_first_line = first_line  # First line of continuation

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
        Process the result data returned by the streaming completion request
        """
        request_data = chat.request_data
        full_response = ""
        completion_tokens = 1  # The following generator misses one, starting from 1 here, to keep the same effect as not opening stream
        # Loop section record
        hash_table = {}
        hash_tokens = {}
        loop_start = -1
        loop_length = -1
        loop_count = 1
        can_continue = False  # Whether it can continue
        current_model_is_set = False
        try:
            for response in completion:
                response = response.model_dump()  # Convert to dictionary
                if not response.get('id'):  # The first one is empty, skip processing
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
                # TODO: Consider the situation of the following other models
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
                        # If the first one is empty, it means the data is completely empty, directly abort here
                        raise Exception("ChatGPT API returned no text")
                    else:
                        # The last content of the incomplete completion token scene is empty, here only prompt for an exception, directly aborting will cause the problem history record to fail to save, affecting the associated conversation
                        self.logger.warning('ChatGPT API returned no content.')
                        continue
                # Determine loop section
                if content in hash_table:
                    if loop_start != -1 and content == hash_tokens[completion_tokens - loop_length]:
                        if completion_tokens + 1 - loop_start == loop_length * 2:
                            loop_count += 1
                            # loop_count loop count limit
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
        Continuation, continue generation
        """
        self.continue_count += 1
        prompt = ConfigurationService.get_prompt_template(ConfigurationConstant.CONTINUE_PROMPT)
        last_lines = generated_text.splitlines()
        last_line = ''
        # Take the last line of the generated code, add it to the continuation prompt, if it is empty, get it from above
        i = -1
        while last_line.strip() == '' and len(last_lines) > abs(i):
            last_line = '\n'.join(last_lines[i:])
            i -= 1
        prompt = prompt.format(lastText=last_line)
        self.logger.info(f'gpt continue. {self.continue_count}, prompt: {prompt}')
        continue_request_data = request_data.copy()
        # The response_format mode continuation will cause an infinite loop of empty characters, so remove response_format
        # TODO: See how to optimize it more generically in the future
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
        Construct message list messages according to conversation history
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
        Use large model to answer user questions
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

            # Change to gpt3.5's chat model in chat scenarios
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

            # Whether to mock conversation data
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

            # Change to gpt3.5's chat model in chat scenarios
            messages, prompt_tokens = self.construct_messages(question, context_association)
            chat = ChatPocket(model=self.model, 
                messages=messages,
                temperature=temperature,
                stream=True,
                request_data=request_data)
            # Whether to mock conversation data
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
