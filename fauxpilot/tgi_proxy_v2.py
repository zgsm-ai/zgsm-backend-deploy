#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import os
import re
import time
import traceback
from datetime import datetime
import random

import pytz

from config.log_config import logger
from instances.redisCache import redisCache

from utils.common import (cut_suffix_overlap, cut_repetitive_text, is_python_text,
                          get_completion_cache, completion_make_cache,
                          get_tokenizer_path, load_tokenizer, is_valid_content
                          )

from utils.constant import FIM_INDICATOR, ModelType, WIN_NL, LINUX_NL
from services.completion_line_service import CompletionLineHandler
from services.model_client_service import ModelClientStrategy, OpenAIClientStrategy, LocalClientStrategy
from models import CompletionContextAndIntention

SPIECE_UNDERLINE_EOT = "▁<EOT>"

default_tokenizer_path = 'cgtok/starcoder_tokenizer.json'
MAIN_TOKENIZER = load_tokenizer(get_tokenizer_path(ModelType.MAIN, default_tokenizer_path))
SMALL_TOKENIZER = load_tokenizer(get_tokenizer_path(ModelType.SMALL, default_tokenizer_path))
UEDC_TOKENIZER = load_tokenizer(get_tokenizer_path(ModelType.UEDC, default_tokenizer_path))
completion_line_handler = CompletionLineHandler()

model_client_strategy_map = {
    "openai": ModelClientStrategy(OpenAIClientStrategy()),
    "local": ModelClientStrategy(LocalClientStrategy()),
    "default": ModelClientStrategy(OpenAIClientStrategy()),
}


def init_stop_words_dict():
    """Get default stop_words"""
    with open('config/stop_words.json', 'r') as f:
        stop_words = json.load(f)
        f.close()
    return stop_words


def get_context_token_limit():
    """Get context token limit, if only one value is set, it will be used for both"""
    context_token_limit = os.environ.get("MAX_MODEL_LEN", "1024,256").split(",")
    if len(context_token_limit) == 1:
        context_token_limit *= 2
    return list(map(int, context_token_limit))


class TGIProxyV2:

    def __init__(self):
        self.MAX_MODEL_LEN = get_context_token_limit()
        self.max_tokens = int(os.environ.get("MAX_TOKENS", 100))
        self.stop_words_dict = init_stop_words_dict()
        self.max_model_cost_time = int(os.environ.get("MAX_MODEL_COST_TIME", 2500))
        self.max_cost_time = int(os.environ.get("MAX_COST_TIME", 3000))
        self.cache = redisCache()
        self.completion_cache_time = int(os.environ.get("COMPLETION_CACHE_TIME", 86400))  # Default 1 day
        self.min_prefix_token = int(os.environ.get("MIN_PREFIX_TOKEN", 1000))

        self.request_stop_words = []  # stop_words from request
        self.system_stop_words = []  # default stop_words from json
        self.all_stop_words = []  # request+system
        self.is_windows = False
        self.model = None
        self.is_codellama = False
        self.client = None
        self.client_strategy = None
        self.tokenizer = None
        self.FIM_PREFIX = ""
        self.FIM_MIDDLE = " "
        self.FIM_SUFFIX = ""
        self.FIM_STOP = ["<|endoftext|>"]
        self.main_model_type = 'default'

    # Initialize completion model information
    def init_completion_model_info(self, data):
        main_model_type = os.environ.get('MAIN_MODEL_TYPE')
        if main_model_type:
            self.main_model_type = main_model_type
        self.model, host, api_key = self.get_model_and_host(self.main_model_type)
        self.client_strategy, self.client = self.get_client(host=host, model=self.model, data=data, api_key=api_key)
        self.tokenizer = self.get_tokenizer()
        self.update_fim_tag()

    def get_model_and_host(self, main_model_type):
        if main_model_type == ModelType.OPENAI:
            model = os.environ.get("OPENAI_MODEL", 'DeepSeek-Coder-V2-Lite-Base')
            host = os.environ.get("OPENAI_MODEL_HOST")
            api_key = os.environ.get("OPENAI_MODEL_API_KEY")
        elif main_model_type == ModelType.LOCAL:
            model = os.environ.get("SMALL_MODEL", 'deepseek-coder_6.7b_v23')
            host = os.environ.get("SMALL_MODEL_HOST")
        else:
            model = os.environ.get("OPENAI_MODEL", 'DeepSeek-Coder-V2-Lite-Base')
            host = os.environ.get("OPENAI_MODEL_HOST")
            api_key = os.environ.get("OPENAI_MODEL_API_KEY")
        return model, host, api_key

    def get_client(self, host, model, data, api_key):
        client_strategy = model_client_strategy_map.get(self.main_model_type)
        return client_strategy, client_strategy.get_client(host, model, data, api_key)

    def get_tokenizer(self):
        if self.main_model_type == ModelType.UEDC:
            return UEDC_TOKENIZER
        elif self.main_model_type == ModelType.SMALL:
            return SMALL_TOKENIZER
        else:
            return MAIN_TOKENIZER

    def update_fim_tag(self):
        """
        Update FIM_PREFIX, FIM_MIDDLE, FIM_SUFFIX based on interface data
        """
        self.is_codellama = 'codellama' in self.model.lower() or 'codegen' in self.model.lower()
        is_deepseek = 'deepseek-coder' in self.model.lower()
        if self.is_codellama:
            self.FIM_PREFIX = "<PRE> "
            self.FIM_MIDDLE = " <MID>"
            self.FIM_SUFFIX = " <SUF>"
            self.FIM_STOP = ["</s>", SPIECE_UNDERLINE_EOT, "<EOT>", "▁<MID>", " <MID>"]
        elif is_deepseek:
            self.FIM_PREFIX = ""
            self.FIM_MIDDLE = " "
            self.FIM_SUFFIX = ""
            self.FIM_STOP = ["", "<|EOT|>", "▁<MID>"]

    def convert_nl_to_win(self, s):
        if self.is_windows:
            return s.replace(LINUX_NL, WIN_NL)
        return s

    @staticmethod
    def convert_nl_to_linux(s):
        return s.replace(WIN_NL, LINUX_NL)

    def prepare_stop_words(self, suffix, data=None):
        """
        Process stop_words list method, when suffix is not empty, only use default stop_words
        """
        if data.get('stop'):
            self.request_stop_words.extend(data.get('stop', []))
        self.request_stop_words.extend(self.FIM_STOP)
        self.all_stop_words.extend(self.request_stop_words)
        if os.environ.get("ADD_SYSTEM_STOP_WORDS", "true") == 'true' or not suffix or not len(suffix.strip()):
            # When suffix is empty, add stop_words list to achieve complete code block truncation effect
            # When 2-3 consecutive newline characters appear, it's generally a new code block scenario, used as a stop sign
            # to make the completion content as complete a code block as possible
            self.all_stop_words.extend([LINUX_NL * 3, LINUX_NL * 2])
            language_id = data.get('languageId', data.get('language_id', None))
            if language_id and language_id.lower() in self.stop_words_dict.keys():
                self.system_stop_words = self.stop_words_dict[language_id.lower()]
                self.all_stop_words.extend(list(map(lambda x: LINUX_NL + x,
                                                    self.stop_words_dict.get(language_id.lower(), []))))
        logger.info(f"all_stop_words={self.all_stop_words}")

    def generate(self, data, context_and_intention):
        prompt = data['prompt']

        # Uniform processing of Windows newline characters
        prompt = self.convert_nl_to_linux(prompt)
        suffix = self.convert_nl_to_linux(context_and_intention.suffix)

        # Prepare stop words
        self.prepare_stop_words(suffix, data)

        model_start_time = time.time()
        is_cache = False
        # Get completion cache
        text_cached = get_completion_cache(self.cache, self.completion_cache_time, prompt)
        if len(text_cached):
            text = text_cached
            is_cache = True
        else:
            response = self.client.generate_stream(prompt=prompt,
                                                   max_new_tokens=self.max_tokens,
                                                   stop_sequences=self.all_stop_words,
                                                   temperature=data['temperature'])

            text = self.client_strategy.choices_process(response, context_and_intention, self.max_model_cost_time)
            # Cache prompt and response results
            completion_make_cache(self.cache, self.completion_cache_time, prompt, text)

        # Stop word processing
        text = self.split_code_completion_by_request_stop_word(self.request_stop_words, text)

        text = self.convert_nl_to_win(text)
        choices = [{'text': text}]

        model_end_time = time.time()
        completion = self.construct_completion(model_start_time, model_end_time)

        completion['choices'] = choices
        completion['_is_cache'] = is_cache

        return completion

    @staticmethod
    def split_code_completion_by_request_stop_word(stop_word_list: list, text: str):
        """
        Split the generated text based on stop words in the request
        """
        # If the generated text is empty, return directly
        if not text or not stop_word_list:
            return text

        for stop_word in stop_word_list:
            if stop_word in text:
                text = text.split(stop_word)[0]

        return text

    @staticmethod
    def split_code_completion_by_system_stop_word(stop_word_list: list, generated_text: str):
        """
        Split the generated text based on system stop words
        Only split at the closest system stop word (to prevent excessive truncation)
        """
        if not generated_text or not stop_word_list:
            return generated_text

        min_index = len(generated_text)
        has_stop_word = False

        for stop_word in stop_word_list:
            index = generated_text.find(stop_word)
            if index != -1 and index < min_index:
                min_index = index
                has_stop_word = True

        # If no stop word is found, return the original text
        if not has_stop_word:
            return generated_text

        # Otherwise, truncate at the closest stop word
        return generated_text[:min_index]

    def construct_completion(self, model_start_time=None, model_end_time=None, model_cost_time=0):
        """
        Construct the completion response
        """
        completion = {
            "id": "cmpl-" + "".join([str(random.randint(0, 9)) for _ in range(29)]),
            "object": "text_completion",
            "model": self.model,
            "created": int(time.time()),
            'usage': {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            },
            "_model_cost_time": model_cost_time or int((model_end_time - model_start_time) * 1000) if model_end_time and model_start_time else 0,
        }
        return completion

    @staticmethod
    def get_time_str(st):
        """
        Get formatted time string
        """
        tz = pytz.timezone('Asia/Shanghai')
        dt = datetime.fromtimestamp(st, tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def get_tokens(self, prompt: str) -> list:
        """
        Get tokens from prompt
        """
        return self.tokenizer.encode(prompt).ids if self.tokenizer else []

    def tokens_decode(self, tokens: list) -> str:
        """
        Decode tokens to string
        """
        return self.tokenizer.decode(tokens) if self.tokenizer else ""

    def get_token_num(self, prompt):
        """
        Get the number of tokens in prompt
        """
        return len(self.get_tokens(prompt))

    def get_prompt_template(self, prefix, suffix, code_context=""):
        """
        Get prompt template based on model type
        """
        if FIM_INDICATOR in prefix:
            return f"{self.FIM_PREFIX}{prefix}{self.FIM_MIDDLE}{suffix}{self.FIM_SUFFIX}{code_context}"
        else:
            return f"{prefix}{code_context}"

    def prepare_prompt(self, prefix, suffix, code_context=""):
        """
        Prepare prompt for model
        """
        if not self.tokenizer:
            return prefix

        # Get original prompt
        prompt = self.get_prompt_template(prefix, suffix, code_context)

        # Get total token count
        prompt_token_num = self.get_token_num(prompt)

        # If the prompt is too long, truncate prefix and recalculate
        if prompt_token_num > self.MAX_MODEL_LEN[0]:
            prefix = self.handle_prompt(prefix, is_prefix=True, optional_prompt=suffix, min_prompt_token=self.min_prefix_token)
            prompt = self.get_prompt_template(prefix, suffix, code_context)

        return prompt

    def handle_prompt(self, prompt, is_prefix=True, optional_prompt=None, min_prompt_token=1000):
        """
        Handle prompt length processing
        """
        # If no tokenizer, return original prompt
        if not self.tokenizer:
            return prompt

        # Check if prompt is within token limits
        token_limit = self.MAX_MODEL_LEN[0]
        prompt_token_num = self.get_token_num(prompt)

        # If optional prompt exists, calculate its token count
        optional_token_num = 0
        if optional_prompt:
            optional_token_num = self.get_token_num(optional_prompt)

        # Check if total length exceeds limit
        if prompt_token_num + optional_token_num > token_limit:
            # Calculate how many tokens to keep
            if is_prefix:
                # When truncating prefix, keep some minimum tokens
                if token_limit - optional_token_num < min_prompt_token and optional_token_num <= token_limit:
                    tokens_to_keep = min_prompt_token
                else:
                    tokens_to_keep = token_limit - optional_token_num

                # Get prompt tokens
                prompt_tokens = self.get_tokens(prompt)

                # If prefix is too long, truncate from the beginning
                if prompt_token_num > tokens_to_keep:
                    truncated_tokens = prompt_tokens[-tokens_to_keep:]
                    truncated_text = self.tokens_decode(truncated_tokens)

                    # Find the first newline to ensure clean split
                    first_newline_index = truncated_text.find('\n')
                    if first_newline_index != -1:
                        truncated_text = truncated_text[first_newline_index + 1:]

                    return truncated_text
            else:
                # When truncating suffix, simply truncate to fit
                tokens_to_keep = max(0, token_limit - prompt_token_num)

                # Get suffix tokens and truncate
                suffix_tokens = self.get_tokens(optional_prompt)
                truncated_tokens = suffix_tokens[:tokens_to_keep]

                return self.tokens_decode(truncated_tokens)

        # If no truncation needed, return original
        return prompt

    def __call__(self, data: dict):
        """
        Main entry point for processing completion requests
        """
        request_data = copy.deepcopy(data)

        # Initialize model info
        self.init_completion_model_info(data)

        try:
            # Default parameters
            if not data.get('temperature'):
                data['temperature'] = float(os.environ.get('CODE_COMPLETION_TEMPERATURE', 0.2))

            # Process prefix and suffix
            prefix_suffix = request_data.get('prefix_suffix', False)
            prefix = request_data.get('prefix', '')
            suffix = request_data.get('suffix', '')
            code_context = request_data.get('code_context', '')

            # Check for Windows line endings
            self.is_windows = prefix.find(WIN_NL) >= 0

            # Prepare context and intention object
            context_and_intention = CompletionContextAndIntention()
            context_and_intention.st = time.time()
            context_and_intention.prefix = prefix
            context_and_intention.suffix = suffix

            # Handle FIM processing
            if prefix_suffix:
                data['prompt'] = self.prepare_prompt(prefix, suffix, code_context)
            else:
                data['prompt'] = prefix

            # Generate completion
            completion = self.generate(data, context_and_intention)

            # Calculate total time
            completion['_total_cost_time'] = int((time.time() - context_and_intention.st) * 1000)

            # Add debug info in development
            if os.environ.get('ENV') != 'production':
                completion['_debug'] = {
                    'prompt': data['prompt'],
                    'prefix': prefix,
                    'suffix': suffix
                }

            return completion

        except Exception as e:
            # Handle exceptions and return error response
            error_info = traceback.format_exc()
            logger.error(f"Error processing completion request: {error_info}")

            return {
                "id": "cmpl-" + "".join([str(random.randint(0, 9)) for _ in range(29)]),
                "object": "text_completion",
                "created": int(time.time()),
                "model": self.model,
                "error": str(e),
                "choices": [{"text": ""}]
            }
