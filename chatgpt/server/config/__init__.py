#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 刘鹏 z10807
    :更新时间: 2023/4/21 15:22
"""
import os
import re

import yaml
from dotenv import load_dotenv

from common.constant import ServeConstant

load_dotenv()


# 线上
# 千流AI
# Client ID：163777834
# Client Secret：c0885d9f91a833d61d549165bf261655

class BaseConfigModel:
    def __init__(self, data=None):
        self._set_default_attr()
        if data is not None:
            self.update(data)

    def _set_default_attr(self):
        for key in dir(self):
            attr = getattr(self, key)
            if key[0] == '_' or hasattr(attr, '__call__'):
                continue
            self.__setattr__(key, attr)

    def update(self, d):
        if not d:
            return
        for k, v in d.items():
            if isinstance(v, dict) and self.__dict__.__contains__(k):
                self.__dict__[k].update(v)
            else:
                self.__setattr__(k, v)

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def get(self, k, default=None):
        return self.__getitem__(k, default)

    def keys(self):
        return self.__dict__.keys()

    def pop(self, *args, **kwargs):
        return self.__dict__.pop(*args, **kwargs)

    def __setattr__(self, k, v):
        if isinstance(v, dict):
            self.__dict__[k] = BaseConfigModel(v)
        else:
            if isinstance(v, str) and self.match_key(v) is not None:
                v = self.get_env_value(self.match_key(v))
            self.__dict__[k] = v

    def __setitem__(self, *args, **kwargs):
        return self.__setattr__(*args, **kwargs)

    def __getitem__(self, k, default=None):
        return self.__dict__.get(k, default)

    # 支持从系统环境变量中获取配置 格式为 redis_host: ${redis_host:xxx.xxx.xxx} 冒号前为环境变量配置值，后边为default_value
    # 支持从yml文件中配置默认参数 如果系统环境变量中不存在所需的配置值，就获取default_val填充。default_val可不写，如redis_host: ${redis_host}
    # 环境变量 Key 中不允许包含 ":"    默认值中允许包含 ":"
    def match_key(self, string):
        p2 = re.compile(r'[$][{](.*)[}]', re.S)  # 最外匹配
        if re.findall(p2, string).__len__() > 0:
            return re.findall(p2, string)[0]
        else:
            return None

    def get_env_value(self, key):
        if key is None:
            return None
        env_dist = os.environ
        value_list = key.split(':', 1)
        if value_list.__len__() > 1:
            env_key = value_list[0]
            if env_key not in env_dist.keys():
                return value_list[1]
            else:
                return env_dist[env_key]
        else:
            if value_list[0] in env_dist.keys():
                return env_dist[value_list[0]]
            return None

    def __iter__(self):
        return iter(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__


class Config:
    # 不按环境变量改动与更新的配置文件
    buildin_config = ['logging', 'ut']

    runtime_path = os.path.dirname(os.path.relpath(__file__))

    def __init__(self, env_name='FLASK_ENV', default_env='development'):
        self.project_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
        self.env_name = os.environ.get(env_name, default_env)
        self.env = self.env_name if self.env_name else default_env
        self.redis_pool = None
        self.archive_es = None
        self.load()

    def load(self):
        for config_file in os.listdir(self.runtime_path):
            if config_file[-4:] == '.yml':
                config_name = config_file[0:-4]
                cfg = self._load_file(config_file, config_name in self.buildin_config)
                if config_name not in self.buildin_config:
                    cfg = BaseConfigModel(cfg)
                setattr(self, config_name, cfg)
        self._load_custom()

    def _load_custom(self):
        config_name = os.environ.get("CUSTOM_CONFIG_FILE", "/custom.yml")
        if config_name != '':
            self.update(self._load_file(config_name, True))

    def _load_file(self, filename, raw):
        path = os.path.join(self.runtime_path, filename)
        if not os.path.isfile(path):
            return {}
        with open(path, 'r', encoding='utf-8') as stream:
            try:
                cfg = yaml.safe_load(stream)
                if cfg is None:
                    return {}
                if raw:
                    return cfg
                else:
                    return cfg.get(self.env, {})
            except Exception as err:
                print(err)
                raise Exception('failed to load config file: {}'.format(path))

    def update(self, d):
        if not d:
            return
        for k, v in d.items():
            if self.__dict__.__contains__(k):
                self.__dict__[k].update(v)
            else:
                getattr(self, k).update(v)


def get_config():
    return {
        "openai_api_key": os.environ.get("OPENAI_API_KEY"),
        "openai_api_base": os.environ.get("OPENAI_API_BASE"),
        "chatgpt_email": os.environ.get("CHATGPT_EMAIL"),
        "chatgpt_password": os.environ.get("CHATGPT_PASSWORD"),
        "redis_url": os.environ.get("REDIS_URL"),
        "database_uri": os.environ.get("DATABASE_URI"),
        "jwt_secret": os.environ.get("JWT_SECRET", "devopssecretversion1.3"),
        "default_cache_expire_seconds": os.environ.get("DEFAULT_CACHE_EXPIRE_SECONDS", 60 * 60 * 24),
        "default_model_name": os.environ.get("DEFAULT_MODEL_NAME", "deepseek-chat"),
        "serve_threads": os.environ.get("SERVE_THREADS", ServeConstant.THREADS),
        "serve_connection_limit": os.environ.get("SERVE_CONNECTION_LIMIT", ServeConstant.CONNECTION_LIMIT),
        "client_id": os.environ.get("CLIENT_ID", "4114011746"),
        "secret": os.environ.get("SECRET", "a75746e1468433bbee364beb3e3069b0"),
        "flask_config": {
            "SECRET_KEY": "ai"
        },
        "jwt": {
            "SECRET": "devopssecretversion1.3",
            "NAME": "ep_jwt_token",
            "EXPIRE": 7,
            "DOMAIN": ".sangfor.com",
            "ALGORITHM": "HS256",
        },
        "user_agent": os.environ.get("USER_AGENT"),
        "es_server": os.environ.get("ES_SERVER"),
        "log_debug": os.environ.get("LOG_DEBUG", False),
        "mock_complation": os.environ.get("MOCK_COMPLATION", False),
        "openai_api_type": os.environ.get("OPENAI_API_TYPE", ServeConstant.DEFAULT_API_TYPE),
        "azure_default_deployment_id": os.environ.get("AZURE_DEFAULT_DEPLOYMENT_ID"),
        "azure_gpt35_deployment_id": os.environ.get("AZURE_GPT35_DEPLOYMENT_ID"),
        "azure_gpt35_16k_deployment_id": os.environ.get("AZURE_GPT35_16K_DEPLOYMENT_ID"),
        "azure_gpt4_deployment_id": os.environ.get("AZURE_GPT4_DEPLOYMENT_ID"),
        "azure_gpt4o_deployment_id": os.environ.get("AZURE_GPT4O_DEPLOYMENT_ID"),
        "openai_api_version": os.environ.get("OPENAI_API_VERSION"),
        "qdrant_server": os.environ.get("QDRANT_SERVER"),
        "chat_timeout": os.environ.get("CHAT_TIMEOUT", 120)
    }


conf = get_config()
CONFIG = Config()
