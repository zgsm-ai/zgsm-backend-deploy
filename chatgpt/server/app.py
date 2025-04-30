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
    '/favicon.ico', # Skip validation logic when accessing the icon
    '/api/test',
    '/api/sessions/idtrust',
    '/api/sessions/idtrust_callback',
    # '/api/users/current'
    # TODO: Context update interface for agent process, used by dify, will consider authentication later
    '/api/configuration',
    '/api/v4/agent/context',
    "/api/inference/v1/chat/completions",
    "/api/inference/v1/completions",
    "/api/inference/v1/embeddings"
]

def software_version():
    """
    Get software version
    Normally, the software version is defined in the code and maintained by programmers as the software code changes.
    In special cases, system administrators can define the version number through the CHATGPT_VERSION environment variable.
    """
    if "CHATGPT_VERSION" in os.environ:
        return os.environ["CHATGPT_VERSION"]
    else:
        return CHATGPT_VERSION

def print_logo():
    try:
        print("""

    ███████╗ ██╗  ██╗███████╗███╗   ██╗███╗   ███╗ █████╗          █████╗ ██╗
    ██╔════╝ ██║  ██║██╔════╝████╗  ██║████╗ ████║██╔══██╗        ██╔══██╗██║
    ██████╗  ███████║█████╗  ██╔██╗ ██║██╔████╔██║███████║ █████╗ ███████║██║
    ╚════██╗ ██╔══██║██╔══╝  ██║╚██╗██║██║╚██╔╝██║██╔══██║ ╚════  ██╔══██║██║
    ███████║ ██║  ██║███████╗██║ ╚████║██║ ╚═╝ ██║██║  ██║        ██║  ██║██║
    ╚══════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝        ╚═╝  ╚═╝╚═╝
        """)
        print(f"    version:  {software_version()}")
    except UnicodeEncodeError:
        print("SHENMA-AI START")


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
        Validate if the request can pass based on rules
        """
        access = True
        # API blacklist rules
        current_path = request.path
        access = access and access_by_rules(current_path)
        # Other disabled rules
        # ·····
        if not access:
            return Result.fail(message='Access denied')
        try:
            if current_path in WHITE_LIST_PATHS:
                return
            if current_path.startswith("/admin"):
                return
            if request.path.startswith("/static"):
                return
            # Cross-origin validation
            if request.method == 'OPTIONS':
                return Result.success()
            access_info = ApplicationContext.get_current()
            if not access_info:
                raise Exception('Authentication failed')
            # Cache current request user information to the current request context, data can be accessed using g.current_user
            g.current_user = access_info
            g.authorization = request.headers.get("Authorization", None)
        except Exception as err:
            app.logger.error(f'Unauthorized: {str(err)}, path: {current_path}, headers: {request.headers.__dict__}')
            if not request.headers.get('api-key'):
                # Here's an update prompt for historical versions of the plugin, old versions don't have api-key
                return make_response('Detected that the current plugin version is not the latest, please open the "Extensions" page and upgrade the plugin version.', 401)
            else:
                return make_response('Unauthorized: Authentication failed, please log in again', 401)


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
        Empty
        ---
        tags:
        - system
        responses:
        200:
            result: Result
        """
        return "hello"

    @app.route("/models")
    def models():
        """
        Model list
        ---
        tags:
        - LLM
        responses:
        200:
            result: Result
        """
        return make_response(jsonify(MODELS))


    register_controller(app)
    return app
