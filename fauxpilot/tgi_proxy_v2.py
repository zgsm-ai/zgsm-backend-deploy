#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import os
import re
import time
import traceback
from datetime import datetime

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
    """Get context token limit, if only one value is set, it is shared"""
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

        self.request_stop_words = []  # Request transmission stop_words
        self.system_stop_words = []  # json default stop_words
        self.all_stop_words = []  # request+system
        self.is_windows = False
        self.model = None
        self.is_codellama = False
        self.client = None
        self.client_strategy = None
        self.tokenizer = None
        self.FIM_PREFIX = "<｜fim▁begin｜>"
        self.FIM_MIDDLE = "<｜fim▁end｜>"
        self.FIM_SUFFIX = "<｜fim▁hole｜>"
        self.FIM_STOP = ["<|endoftext|>"]
        self.main_model_type = 'default'

    # Initialize the completion model information
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
        Update FIM_PREFIX, FIM_MIDDLE, FIM_SUFFIX according to interface data
        """
        self.is_codellama = 'codellama' in self.model.lower() or 'codegen' in self.model.lower()
        is_deepseek = 'deepseek-coder' in self.model.lower()
        if self.is_codellama:
            self.FIM_PREFIX = "<PRE> "
            self.FIM_MIDDLE = " <MID>"
            self.FIM_SUFFIX = " <SUF>"
            self.FIM_STOP = ["</s>", SPIECE_UNDERLINE_EOT, "<EOT>", "▁<MID>", " <MID>"]
        elif is_deepseek:
            self.FIM_PREFIX = "<｜fim▁begin｜>"
            self.FIM_MIDDLE = "<｜fim▁end｜>"
            self.FIM_SUFFIX = "<｜fim▁hole｜>"
            self.FIM_STOP = ["<｜end▁of▁sentence｜>", "<|EOT|>", "▁<MID>"]

    def convert_nl_to_win(self, s):
        if self.is_windows:
            return s.replace(LINUX_NL, WIN_NL)
        return s

    @staticmethod
    def convert_nl_to_linux(s):
        return s.replace(WIN_NL, LINUX_NL)

    def prepare_stop_words(self, suffix, data=None):
        """
        Handle stop_words list method, when the suffix is not empty, only the default stop_words are used
        """
        if data.get('stop'):
            self.request_stop_words.extend(data.get('stop', []))
        self.request_stop_words.extend(self.FIM_STOP)
        self.all_stop_words.extend(self.request_stop_words)
        if os.environ.get("ADD_SYSTEM_STOP_WORDS", "true") == 'true' or not suffix or not len(suffix.strip()):
            # When the suffix is empty, add the stop_words list to achieve complete code block truncation effect
            # When 2~3 line breaks appear consecutively, it is generally a new code block scenario, which is used as a stop sign, so that the completed content is as complete as possible
            self.all_stop_words.extend([LINUX_NL * 3, LINUX_NL * 2])
            language_id = data.get('languageId', data.get('language_id', None))
            if language_id and language_id.lower() in self.stop_words_dict.keys():
                self.system_stop_words = self.stop_words_dict[language_id.lower()]
                self.all_stop_words.extend(list(map(lambda x: LINUX_NL + x,
                                                    self.stop_words_dict.get(language_id.lower(), []))))
        logger.info(f"all_stop_words={self.all_stop_words}")

    def generate(self, data, context_and_intention):
        prompt = data['prompt']

        # Unified processing of windows line breaks
        prompt = self.convert_nl_to_linux(prompt)
        suffix = self.convert_nl_to_linux(context_and_intention.suffix)

        # Stop word preparation
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

        completion['completion_tokens'] = self.get_token_num(text)

        return completion, choices, is_cache

    @staticmethod
    def split_code_completion_by_request_stop_word(stop_word_list: list, text: str):
        """
        Truncated processing based on request parameter stop_words
        """
        for stop_word in stop_word_list:
            if stop_word in text:
                text = text.split(stop_word, 1)[0]
            if stop_word == SPIECE_UNDERLINE_EOT and len(text) > 1 and text[-1] == text[-2]:
                text = text[:-1]
        return text

    @staticmethod
    def split_code_completion_by_system_stop_word(stop_word_list: list, generated_text: str):
        """
        Truncated processing based on system default stop_words
        Consider \n + zero or more spaces scenario
        """
        match_list = list()
        if stop_word_list and len(stop_word_list) == 0:
            return generated_text
        for stop_word in stop_word_list:
            # If the end word is a single line break, directly match the line break
            if stop_word in ['\n', '\r']:
                pattern = r'^.*?(?=' + stop_word + r')'
            #  There are normal end words, matching strings starting with \n and containing 0~n spaces in the middle, and ending with stop_word
            else:
                pattern = r'^.*?(?=\n\s{0,4}' + stop_word + r')'
            match = re.search(pattern, generated_text, re.DOTALL | re.MULTILINE)
            if match:
                match_list.append(match.group(0))

        # Returns the shortest match
        cut_generated_text = ""
        if match_list:
            cut_generated_text = min(match_list, key=len)
        cut_generated_text = cut_generated_text if cut_generated_text else generated_text
        return cut_generated_text

    def construct_completion(self, model_start_time=None, model_end_time=None, model_cost_time=0):
        if model_start_time and model_end_time:
            model_cost_time = int((model_end_time - model_start_time) * 1000)
        if model_start_time:
            model_start_time = self.get_time_str(model_start_time)
        if model_end_time:
            model_end_time = self.get_time_str(model_end_time)
        return {
            'id': None,  # fill in
            'model': self.model,
            'object': 'text_completion',
            'created': int(time.time()),
            'choices': None,  # fill in
            'model_start_time': model_start_time,
            'model_end_time': model_end_time,
            'model_cost_time': model_cost_time
        }

    @staticmethod
    def get_time_str(st):
        """Get the formatted string of time"""
        dt = datetime.fromtimestamp(st)
        dt_in_shanghai = dt.astimezone(pytz.timezone('Asia/Shanghai'))
        time_str = dt_in_shanghai.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return time_str

    def get_tokens(self, prompt: str) -> list:
        """Get tokens encoding list"""
        tokens = self.tokenizer.encode(prompt)
        return tokens.ids

    def tokens_decode(self, tokens: list) -> str:
        """
        Decode tokens encoding list to prompt
        tokens：encoding list
        """
        return self.tokenizer.decode(tokens)

    def get_token_num(self, prompt):
        """Get the number of tokens"""
        return len(self.get_tokens(prompt))

    def get_prompt_template(self, prefix, suffix, code_context=""):
        """
        prompt splicing strategy
        :param prefix:
        :param suffix:
        :param code_context
        :return:
        """
        return f"{self.FIM_PREFIX}{code_context}\n{prefix}{self.FIM_SUFFIX}{suffix}{self.FIM_MIDDLE}"

    def prepare_prompt(self, prefix, suffix, code_context=""):
        """
         After processing the length of the prefix and suffix, splice the prompt
        :param prefix:
        :param suffix:
        :param code_context:
        :return:
        """
        prefix, code_context = self.handle_prompt(prompt=prefix, is_prefix=True,
                                                  optional_prompt=code_context,
                                                  min_prompt_token=self.min_prefix_token)
        suffix, _ = self.handle_prompt(prompt=suffix, is_prefix=False)
        prompt = self.get_prompt_template(prefix, suffix, code_context)
        prompt_tokens = self.get_token_num(prompt)
        self.is_windows = WIN_NL in prefix
        return prompt, prompt_tokens, prefix, suffix

    def handle_prompt(self, prompt, is_prefix=True, optional_prompt=None, min_prompt_token=1000):
        """
        If the prompt exceeds the maximum number of tokens, truncate it
        The prefix truncates the front part
        The suffix truncates the back part
        :param prompt:
        :param is_prefix:
        :param optional_prompt: Extra context
        :param min_prompt_token: How many tokens should the prompt keep at least
        :return: prompt, optional_prompt
        """
        optional_prompt_tokens = 0
        requested_tokens = self.get_token_num(prompt)
        if optional_prompt:
            optional_prompt_tokens = self.get_token_num(optional_prompt)
        max_model_len = self.MAX_MODEL_LEN[0] if is_prefix else self.MAX_MODEL_LEN[1]

        if requested_tokens + optional_prompt_tokens > max_model_len:
            prompt_tokens = self.get_tokens(prompt)
            need_cut_tokens = requested_tokens + optional_prompt_tokens - max_model_len

            truncated_tokens = None
            truncated_optional_tokens = None

            # If the number of remaining tokens is greater than the minimum number of tokens after truncating the prefix, truncate the prompt directly
            if is_prefix and requested_tokens - need_cut_tokens >= min_prompt_token:
                truncated_tokens = prompt_tokens[need_cut_tokens:]
            # If the number of remaining tokens is less than the minimum number of tokens after truncating the prefix, truncate to keep the minimum number of tokens, and then truncate optional_prompt
            elif is_prefix and requested_tokens - need_cut_tokens < min_prompt_token:
                # Keep the minimum number of tokens (worry that the prefix is less than min_prompt_token, resulting in reduced context content)
                actual_min = min(min_prompt_token, requested_tokens)
                truncated_tokens = prompt_tokens[-actual_min:]
                optional_token = self.get_tokens(optional_prompt)
                truncated_optional_tokens = optional_token[:(max_model_len - actual_min)]
            elif not is_prefix:
                truncated_tokens = prompt_tokens[:-need_cut_tokens]

            # Decode the truncated tokens back to a string
            if truncated_tokens:
                prompt = self.tokens_decode(truncated_tokens)

            if truncated_optional_tokens:
                optional_prompt = self.tokens_decode(truncated_optional_tokens)

            # Ensure that the cut is a complete line, if it is not complete, remove it
            lines = prompt.splitlines(True)
            if len(lines) > 0:
                if is_prefix:  # Prefix processing first line
                    if any([lines[0].startswith('\n'), lines[0].startswith('\r\n')]) is False:
                        lines = lines[1:]
                else:  # Suffix processing last line
                    if any([lines[-1].endswith('\n'), lines[-1].endswith('\r\n')]) is False:
                        lines = lines[:-1]
                prompt = ''.join(lines)

        return prompt, optional_prompt

    def __call__(self, data: dict):
        st = time.time()
        is_cache = False
        is_same = True
        model_choices = []
        prefix, suffix = '', ''
        if data['prompt_options']:
            prefix = data['prompt_options']['prefix']
            suffix = data['prompt_options']['suffix']
            cursor_line_prefix = data['prompt_options']['cursor_line_prefix']
            cursor_line_suffix = data['prompt_options']['cursor_line_suffix']
            code_context = data['prompt_options']['code_context']
        else:
            prompt_split = data['prompt'].split(FIM_INDICATOR)
            if prompt_split and len(prompt_split) >= 2:
                prefix = prompt_split[-2]
                suffix = prompt_split[-1]
            cursor_line_prefix = prefix.split('\n')[-1]
            split_suffix = suffix.split('\n')
            cursor_line_suffix = split_suffix[0]
            if len(split_suffix) > 1:
                cursor_line_suffix += '\n'
            code_context = data.get('code_context', '')
        language = data.get("language_id")
        try:
            # Completion model initialization (model strategy selection, tokenizer initialization, special token initialization, etc.)
            self.init_completion_model_info(data)
            logger.info(f"model={self.model}, self.FIM_PREFIX={self.FIM_PREFIX}")

            # Completion pre-processing (prompt splicing strategy, single-line/multi-line completion strategy)
            prompt, prompt_tokens, prefix, suffix = self.prepare_prompt(prefix, suffix, code_context)
            data['prompt'] = prompt
            data['prompt_tokens'] = prompt_tokens

            is_single_completion = completion_line_handler.judge_single_completion(
                cursor_line_prefix, cursor_line_suffix, language)
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"

            logger.info(f"language={language}, is_single_completion={is_single_completion}")

            # Request completion
            if prompt_tokens > 0:
                context_and_intention = CompletionContextAndIntention(
                    language=language,
                    is_single_completion=is_single_completion,
                    prefix=prefix,
                    suffix=suffix,
                    cursor_line_prefix=cursor_line_prefix,
                    cursor_line_suffix=cursor_line_suffix,
                    st=st,
                )
                completion, choices, is_cache = self.generate(data, context_and_intention)
            else:
                logger.info(f"{data['x-complete-id']} no line use to completion after prepare!")
                completion = self.construct_completion()
                choices = []
                prompt_tokens = 0

        except Exception:
            logger.error(traceback.format_exc())
            completion = self.construct_completion()
            choices = []
            prompt_tokens = 0

        # Completion post-processing - content discarding
        if choices:
            model_choices = copy.deepcopy(choices)

        # if choices and check_context_include_text(choices[0]['text'], prefix, suffix):
        #     logger.info(f"{data['x-complete-id']} exist context, return empty choices!")
        #     choices = []

        if (choices and data.get("language_id") and
                str(data.get("language_id")).lower() != 'python' and
                is_python_text(choices[0].get('text', ''))):
            choices = []

        # Completion post-processing - completion content processing
        if choices and choices[0]['text']:
            text = choices[0].get('text', '')

            # Completion content deduplication
            text = cut_repetitive_text(text)

            # Completion content overlap clipping
            text = cut_suffix_overlap(text, prefix, suffix)

            # The logic of syntax post-processing has been changed to streaming process processing
            # See: https://ipd.atrust.sangfor.com/ipd/team/7768/board?group_by=assigner&issue_type=global
            # # In the single-line completion scenario and there are invalid parentheses, the parenthesis mismatch processing is performed on the complete line where the completion content is located
            # if is_single_completion and not is_valid_brackets(cursor_line_prefix + text + cursor_line_suffix):
            #     text = cut_text_by_tree_sitter(language, text, cursor_line_prefix, cursor_line_suffix, st,
            #                                    self.max_cost_time)
            #
            # # Prefix + suffix + complete completion content for syntax verification, and cut if not satisfied
            # text = cut_text_by_tree_sitter(language, text, prefix, suffix, st,
            #                                self.max_cost_time)

            # If there is no actual completion content, set it to empty
            if not is_valid_content(text):
                text = ""
            if text != choices[0]['text']:
                logger.info(f"Trigger completion post-processing completed, the processed result is as follows: {text}")
            choices[0]['text'] = text

        if model_choices and model_choices[0].get('text') and choices != model_choices:
            is_same = False

        ed = time.time()
        completion['cost_time'] = int((ed - st) * 1000)
        completion['start_time'] = self.get_time_str(st)
        completion['end_time'] = self.get_time_str(ed)
        completion['prompt_tokens'] = prompt_tokens
        completion['max_token'] = self.max_tokens
        completion['id'] = data['x-complete-id']
        completion['prompt'] = data['prompt']
        completion['choices'] = choices
        completion['is_same'] = is_same
        completion['model_choices'] = model_choices
        completion['server_extra_kwargs'] = {
            'is_cache': is_cache,
            'score': data.get("score"),
        }
        completion['user_code_upload_delay'] = int(os.environ.get("USER_CODE_UPLOAD_DELAY", "0"))
        completion['code_context_strategy'] = data.get('code_context_strategy')
        # System plugin configuration, used to update the default configuration of the plugin end
        completion['system_plugin_configs'] = {
            'context_lines_limit': int(os.environ.get("CONTEXT_LINES_LIMIT", "80")),
            'one_file_max_length': int(os.environ.get('ONE_FILE_MAX_LENGTH', '10000')),
            'total_file_max_length': int(os.environ.get('TOTAL_FILE_MAX_LENGTH', '200000')),
            'import_max_number': int(os.environ.get('IMPORT_MAX_NUMBER', '10')),
            'file_max_number': int(os.environ.get('FILE_MAX_NUMBER', '20')),
            'window_length': int(os.environ.get('WINDOWS_LENGTH', '60')),
            'score_threshold': float(os.environ.get('SCORE_THRESHOLD', '0.15')),
            'snippet_top_n': int(os.environ.get('SNIPPET_TOP_N', '0')),
            'code_completion_log_upload_once': bool(int(os.environ.get('CODE_COMPLETION_LOG_UPLOAD_ONCE', '0'))),
            'suggestion_delay': int(os.environ.get('SUGGESTION_DELAY', '75')),
        }
        logger.info(f"{data['x-complete-id']} Returned completion in {(ed - st) * 1000} ms")
        # Unified response, no longer supports client-side streaming response
        return json.dumps(completion)
