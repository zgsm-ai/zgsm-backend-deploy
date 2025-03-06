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
    """获取默认stop_words"""
    with open('config/stop_words.json', 'r') as f:
        stop_words = json.load(f)
        f.close()
    return stop_words


def get_context_token_limit():
    """获取上下文token数限制，如只设置一个值，则共用"""
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
        self.completion_cache_time = int(os.environ.get("COMPLETION_CACHE_TIME", 86400))  # 默认1天
        self.min_prefix_token = int(os.environ.get("MIN_PREFIX_TOKEN", 1000))

        self.request_stop_words = []  # 请求传输stop_words
        self.system_stop_words = []  # json默认stop_words
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

    # 初始化补全模型信息
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
        根据接口数据更新FIM_PREFIX、FIM_MIDDLE、FIM_SUFFIX
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
        处理stop_words列表方法，当后缀非空时，只用默认的stop_words
        """
        if data.get('stop'):
            self.request_stop_words.extend(data.get('stop', []))
        self.request_stop_words.extend(self.FIM_STOP)
        self.all_stop_words.extend(self.request_stop_words)
        if os.environ.get("ADD_SYSTEM_STOP_WORDS", "true") == 'true' or not suffix or not len(suffix.strip()):
            # 当后缀为空时添加stop_words列表实现完整代码块截断效果
            # 当连续出现2~3个换行符号时，一般是新起代码块场景，作为stop标志符号，使补全内容尽可能是完整代码块
            self.all_stop_words.extend([LINUX_NL * 3, LINUX_NL * 2])
            language_id = data.get('languageId', data.get('language_id', None))
            if language_id and language_id.lower() in self.stop_words_dict.keys():
                self.system_stop_words = self.stop_words_dict[language_id.lower()]
                self.all_stop_words.extend(list(map(lambda x: LINUX_NL + x,
                                                    self.stop_words_dict.get(language_id.lower(), []))))
        logger.info(f"all_stop_words={self.all_stop_words}")

    def generate(self, data, context_and_intention):
        prompt = data['prompt']

        # windows换行符统一处理
        prompt = self.convert_nl_to_linux(prompt)
        suffix = self.convert_nl_to_linux(context_and_intention.suffix)

        # 停用词准备
        self.prepare_stop_words(suffix, data)

        model_start_time = time.time()
        is_cache = False
        # 获取completion缓存
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
            # 缓存prompt 和 响应结果
            completion_make_cache(self.cache, self.completion_cache_time, prompt, text)

        # stop word处理
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
        根据请求参数 stop_words 截断处理
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
        根据系统默认 stop_words 截断处理
        考虑 \n + 零或多个空格 场景
        """
        match_list = list()
        if stop_word_list and len(stop_word_list) == 0:
            return generated_text
        for stop_word in stop_word_list:
            # 如果结束词是单个换行，直接匹配换行符
            if stop_word in ['\n', '\r']:
                pattern = r'^.*?(?=' + stop_word + r')'
            #  有正常结束词,匹配以\n开头中间包含0~n个空格，再以stop_word为末尾的字符串
            else:
                pattern = r'^.*?(?=\n\s{0,4}' + stop_word + r')'
            match = re.search(pattern, generated_text, re.DOTALL | re.MULTILINE)
            if match:
                match_list.append(match.group(0))

        # 返回最短的匹配
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
        """获取时间的格式化字符串"""
        dt = datetime.fromtimestamp(st)
        dt_in_shanghai = dt.astimezone(pytz.timezone('Asia/Shanghai'))
        time_str = dt_in_shanghai.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return time_str

    def get_tokens(self, prompt: str) -> list:
        """获取 tokens 编码列表"""
        tokens = self.tokenizer.encode(prompt)
        return tokens.ids

    def tokens_decode(self, tokens: list) -> str:
        """
        将 tokens 编码列表 解码为 prompt
        tokens：编码列表
        """
        return self.tokenizer.decode(tokens)

    def get_token_num(self, prompt):
        """获取token数量"""
        return len(self.get_tokens(prompt))

    def get_prompt_template(self, prefix, suffix, code_context=""):
        """
        prompt拼接策略
        :param prefix:
        :param suffix:
        :param code_context
        :return:
        """
        return f"{self.FIM_PREFIX}{code_context}\n{prefix}{self.FIM_SUFFIX}{suffix}{self.FIM_MIDDLE}"

    def prepare_prompt(self, prefix, suffix, code_context=""):
        """
         前后缀长度处理后对prompt进行拼接
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
        如果prompt超过最大token数，则截断它
        前缀截掉前面部分
        后缀截掉后面部分
        :param prompt:
        :param is_prefix:
        :param optional_prompt: 额外上下文
        :param min_prompt_token: 至少保留prompt多少token
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

            # 如果截断前缀后，剩余的token数大于最小token数，则直接截断prompt
            if is_prefix and requested_tokens - need_cut_tokens >= min_prompt_token:
                truncated_tokens = prompt_tokens[need_cut_tokens:]
            # 如果截断前缀后，剩余的token数小于最小token数，则截断保留最小token数，然后截断optional_prompt
            elif is_prefix and requested_tokens - need_cut_tokens < min_prompt_token:
                # 保留最小token数（担心前缀小于min_prompt_token，导致关联上下文内容减少）
                actual_min = min(min_prompt_token, requested_tokens)
                truncated_tokens = prompt_tokens[-actual_min:]
                optional_token = self.get_tokens(optional_prompt)
                truncated_optional_tokens = optional_token[:(max_model_len - actual_min)]
            elif not is_prefix:
                truncated_tokens = prompt_tokens[:-need_cut_tokens]

            # 将截断的tokens解码回字符串
            if truncated_tokens:
                prompt = self.tokens_decode(truncated_tokens)

            if truncated_optional_tokens:
                optional_prompt = self.tokens_decode(truncated_optional_tokens)

            # 保证切割处为完整行，若不完整 将其移除
            lines = prompt.splitlines(True)
            if len(lines) > 0:
                if is_prefix:  # 前缀处理首行
                    if any([lines[0].startswith('\n'), lines[0].startswith('\r\n')]) is False:
                        lines = lines[1:]
                else:  # 后缀处理尾行
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
            # 补全模型初始化（模型策略选择，tokenizer初始化，特殊token初始化等）
            self.init_completion_model_info(data)
            logger.info(f"model={self.model}, self.FIM_PREFIX={self.FIM_PREFIX}")

            # 补全前置处理 （拼接prompt策略，单行/多行补全策略）
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

            # 请求补全
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

        # 补全后置处理-内容丢弃
        if choices:
            model_choices = copy.deepcopy(choices)

        # if choices and check_context_include_text(choices[0]['text'], prefix, suffix):
        #     logger.info(f"{data['x-complete-id']} exist context, return empty choices!")
        #     choices = []

        if (choices and data.get("language_id") and
                str(data.get("language_id")).lower() != 'python' and
                is_python_text(choices[0].get('text', ''))):
            choices = []

        # 补全后置处理-补全内容处理
        if choices and choices[0]['text']:
            text = choices[0].get('text', '')

            # 补全内容去重
            text = cut_repetitive_text(text)

            # 补全内容重叠裁剪
            text = cut_suffix_overlap(text, prefix, suffix)

            # 语法后置处理的逻辑已改成了流式过程处理
            # 详见：https://ipd.atrust.sangfor.com/ipd/team/7768/board?group_by=assigner&issue_type=global
            # # 在单行补全场景 且 存在无效的括号 则对补全内容所在的完整行进行括号错配处理
            # if is_single_completion and not is_valid_brackets(cursor_line_prefix + text + cursor_line_suffix):
            #     text = cut_text_by_tree_sitter(language, text, cursor_line_prefix, cursor_line_suffix, st,
            #                                    self.max_cost_time)
            #
            # # 前后缀 + 完整补全内容 进行语法校验, 不满足则进行切割
            # text = cut_text_by_tree_sitter(language, text, prefix, suffix, st,
            #                                self.max_cost_time)

            # 无实际补全内容，置为空
            if not is_valid_content(text):
                text = ""
            if text != choices[0]['text']:
                logger.info(f"触发补全后置处理完成，处理后的结果如下：{text}")
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
        # 系统插件配置，用于更新插件端的默认配置
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
        # 统一响应，不再支持客户端流式响应
        return json.dumps(completion)
