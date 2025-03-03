#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask, request, make_response, jsonify,  g
#from flasgger import Swagger

from admin import register_admin
from common.exception import register_exception
from common.helpers.custom_json_encoder import CustomJSONEncoder
from common.helpers.custom_throttle import register_throttle
from common.helpers.response_helper import Result
from common.constant import  GPTModelConstant
from config import conf
from db import db
from common.helpers.application_context import ApplicationContext
from controllers import register_controller, registry_session
from logger import register_logger

CHATGPT_VERSION = "1.5.9"

MODELS = [
    {
        "label": "gpt-3.5-turbo", "value": GPTModelConstant.GPT_TURBO, "desc": "gpt-3.5-turbo", "default": True
    },
    {
        "label": "gpt-4", "value": GPTModelConstant.GPT_4, "desc": "gpt-4"
    }
]

WHITE_LIST_PATHS = [
    '/favicon.ico', # 图标访问时省掉校验逻辑
    '/api/test',
    '/api/sessions/idtrust',
    '/api/sessions/idtrust_callback',
    # '/api/users/current'
    # TODO agent 过程的 context 更新接口，给 dify 用的，后续再考虑鉴权
    '/api/configuration',
    '/api/v4/agent/context',
    "/api/inference/v1/chat/completions",
    "/api/inference/v1/completions",
    "/api/inference/v1/embeddings"
]

def software_version():
    """
    获取软件版本
    正常情况下软件版本定义在代码中，随着软件代码变更由程序员维护，
    特殊情况下，系统管理员可以通过环境变量CHATGPT_VERSION定义版本号
    """
    if "CHATGPT_VERSION" in os.environ:
        return os.environ["CHATGPT_VERSION"]
    else:
        return CHATGPT_VERSION

def print_logo():
    try:
        print("""
    ███████╗██╗  ██╗██╗   ██╗ ██████╗ ███████╗       █████╗ ██╗
    ╚══███╔╝██║  ██║██║   ██║██╔════╝ ██╔════╝      ██╔══██╗██║
      ███╔╝ ███████║██║   ██║██║  ███╗█████╗  █████╗███████║██║
     ███╔╝  ██╔══██║██║   ██║██║   ██║██╔══╝  ╚════╝██╔══██║██║
    ███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗      ██║  ██║██║
    ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝      ╚═╝  ╚═╝╚═╝
        """)
        print(f"    version:  {software_version()}")
    except UnicodeEncodeError:
        print("ZHUGE-AI START")


def create_app():
    print_logo()
    app = Flask(__name__)
    app.config.update(conf.get("flask_config"))
    # custom json encoder
    app.json_encoder = CustomJSONEncoder
    # # register db mamager
    db.init_app(app)
    register_throttle(app)
    registry_session(app)
    register_admin(app)
    register_exception(app)
    register_logger(app)
    
    app.logger.info("create_app: starting...")

    def access_by_rules(current_path):
        # pylint: disable=no-member
        api_ban_list = conf.get('API_BAN_LIST', list())
        current_path = request.path
        if api_ban_list and current_path in api_ban_list:
            return False
        return True

    @app.before_request
    def check_request():
        """
        根据规则校验请求是否能够通过
        """
        access = True
        # api黑名单规则
        current_path = request.path
        access = access and access_by_rules(current_path)
        # 其他禁用规则
        # ·····
        if not access:
            return Result.fail(message='禁止访问')
        try:
            if current_path in WHITE_LIST_PATHS:
                return
            if current_path.startswith("/admin"):
                return
            if request.path.startswith("/static"):
                return
            # 跨域验证
            if request.method == 'OPTIONS':
                return Result.success()
            access_info = ApplicationContext.get_current()
            if not access_info:
                raise Exception('认证失败')
            # 当前请求用户信息缓存到当前请求上下文，需要使用数据可用 g.current_user 获取
            g.current_user = access_info
            g.authorization = request.headers.get("Authorization", None)
        except Exception as err:
            app.logger.error(f'Unauthorized: {str(err)}, path: {current_path}, headers: {request.headers.__dict__}')
            if not request.headers.get('api-key'):
                # 这里针对插件历史版本提供一个更新提示，老版本无api-key
                return make_response('检测到当前插件版本不是最新版本，请打开"扩展"页面，升级插件版本。', 401)
            else:
                return make_response('Unauthorized: 认证失败，请重新登陆', 401)


    @app.after_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = "true"
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PATCH, DELETE, PUT'
        response.headers['Access-Control-Max-Age'] = '3600'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept,' \
                                                           'Api-Key, ide, ide-version, ide-real-version, host-ip, User-Agent, ' \
                                                           'Model, Authorization, Cookie'
        response.headers['Access-Control-Expose-Headers'] = 'resp_id, mock_stream'
        return response

    def format_prompt_string(string):
        return '{{' + str(string) + '}}'

    @app.route("/")
    def index():
        """
        空
        ---
        tags:
        - system
        responses:
        200:
            result: 结果
        """
        return "hello"

    @app.route("/models")
    def models():
        """
        模型列表
        ---
        tags:
        - LLM
        responses:
        200:
            result: 结果
        """
        return make_response(jsonify(MODELS))


    register_controller(app)
    return app
