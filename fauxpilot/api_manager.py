#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional, Union

import requests
from requests import Response
from config.log_config import logger


class OpenAiServerManager:

    def __init__(
        self,
        url,
        model: str = None,
        api_key: str = None,
        timeout: int = 10,
    ):
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        if api_key is not None:
            self.headers["Authorization"] = "Bearer %s" % api_key
        self.url = url
        self.model = model
        self.timeout = timeout

    def generate_stream(
        self,
        prompt: str,
        n: int = 1,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        temperature: float = 1.0,
        top_p: float = 1.0,
        stop_sequences: Optional[Union[str, List[str]]] = None,
        max_new_tokens: int = 16,
        logprobs: Optional[int] = None,
    ) -> Response | None:
        params = {
            'model': self.model,
            'prompt': prompt,
            'n': n,
            'presence_penalty': presence_penalty,
            'frequency_penalty': frequency_penalty,
            'temperature': temperature,
            'top_p': top_p,
            'stop': stop_sequences if stop_sequences is not None else [],
            'max_tokens': int(max_new_tokens),
            'logprobs': logprobs,
            'stream': True
        }

        response = requests.post(self.url, json=params, headers=self.headers, stream=True)
        if response.status_code != 200:
            logger.error(f'{self.url} request error code: {response.status_code}, {response.text}')
            return None
        return response
