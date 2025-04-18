#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ActionsConstant:
    FIND_BUGS = "findProblems"
    ADD_TEST = "addTests"
    OPTIMIZE = "optimize"
    EXPLAIN = "explain"
    CHAT = "chat"
    ADVISE="advise"
    GENERATE_CODE = "generateCode"
    # e2e case generation========
    REVIEW = "review"
    SCRIBE = "scribe"
    ADD_DEBUG_CODE = "addDebugCode"  # Add debug code
    ADD_STRONGER_CODE = "addStrongerCode"  # Add robustness code
    ADD_COMMENT = "addComment"  # Add comments
    PICK_COMMON_FUNC = "pickCommonFunc"  # Extract common functions
    SIMPLIFY_CODE = "simplifyCode"  # Simplify code
    GIVE_ADVICE = "giveAdvice"  # Give advice
    CONTINUE = "continue"  # Continue writing
    ZHUGE_NORMALCHAT = 'zhuge_normal_chat'  # Zhuge normal chat

class GPTModelConstant:
    GPT_35 = "gpt-3.5"  # Use GPT_35_16K, only used in request parameters
    GPT_TURBO = "gpt-3.5-turbo"  # Use GPT_35_16K, only used in request parameters
    GPT_35_16K = "gpt-35-turbo-16k"  # 16k model
    GPT_4 = "gpt-4"  # 128k model
    GPT_4o = "gpt-4o"  # 128k model
    GPT_35_CHAT_MODELS = [GPT_TURBO, GPT_35_16K]  # List of supported models
    DEEPSEEK_SEEK_CHAT = "deepseek-chat"
    CHAT_MODELS = [GPT_TURBO, GPT_35_16K, GPT_4, GPT_4o, DEEPSEEK_SEEK_CHAT, ]  # List of supported models


class GPTConstant:
    TIMEOUT = 120  # Unit: s
    GPT35_16K_MAX_TOKENS = 12000  # Input limit 12k
    GPT4_MAX_TOKENS = 60000  # Input limit 60k
    DEEPSEEK_SEEK_CHAT_TOKENS = 128000
    # Code generation limits the maximum number of tokens, which should be less than the maximum number of tokens.
    CODE_GENERATE_MAX_PROMPT_TOKENS = GPT35_16K_MAX_TOKENS - 200

    # Response format type
    RESPONSE_JSON_OBJECT = 'json_object'
    RESPONSE_FORMAT_TYPES = [RESPONSE_JSON_OBJECT]  # gpt new version supports list of return format types

    SCRIBE_MAX_PROMPT_TOKENS = 6000  # Word selection dialog limits maximum tokens

    MAX_CONTINUE_COUNT = 2  # Maximum number of allowed continuation writes
    CONTINUE_SIGN = '\n----------Continue----------\n'  # Continuation identifier
    # Allow automatic continuation writing actions
    ALLOW_CONTINUE_ACTIONS = [
        ActionsConstant.CONTINUE,
        ActionsConstant.SCRIBE,
    ]

    # Completion reason
    class FinishReason:
        STOP = 'stop'  # The API returned a complete model output.
        LENGTH = 'length'  # The model output is incomplete due to the max_tokens parameter or token limit.
        CONTENT_FILTER = 'content_filter'  # Content omitted due to content filter flags.
        NULL = 'null'  # The API response is still in progress or incomplete.


class TikTokenEncodeType:
    CL100K_BASE = "cl100k_base"  # ChatGPT models, text-embedding-ada-002, include gpt-3.5-turbo
    P50K_BASE = "p50k_base"  # Code models, text-davinci-002, text-davinci-003
    R50K_BASE = "r50k_base"  # (or gpt2)	GPT-3 models like davinci


class ServeConstant:
    THREADS = 4  # The number of threads that waitress serve uses to handle application logic, the default is 4.
    CONNECTION_LIMIT = 100
    DEFAULT_API_TYPE = "openai"


class NullValueSort:
    """
    Place None value sorting first or last
    """
    NULL_FIRST = 'null_first'
    NULL_LAST = 'null_last'


class AppConstant:
    DELETED = True
    REQUESTS_TIMEOUT_TIME = [2, 4, 8, 16, 32, 64]
    DEPT_CACHE_TIMEOUT = 86400  # Department data cache for 24 hours


class UserRole:
    ADMIN = "admin"  # Administrator
    USER = "user"  # Normal user


class ErrorMsgs:
    TIMEOUT = 'Cancelling nested steps due to timeout'  # The task execution time exceeds the set time, default 60 minutes
    GITLAB_NOT_RESPONDE = 'GitLab is not responding'  # gitlab 502 error key field


class AdminNoticeContent:
    """Admin notice content"""
    CONTENT = 'Qianliu AI notice:\nUser {username} is applying for an API account.\nPlease go to the backend management for approval: {chat_admin_url}'


class ApplicantNoticeContent:
    """Applicant notice content"""
    CONTENT = 'Qianliu AI notice:\n{first_line}{approve_remark}\nApplication name: {project_name}\nExpiration time: {expiration_time}\n' \
              'Reason for application: {application_reason}\nExpected benefits: {expected_profit}\n' \
              'For more operations, please go to the Qianliu AI platform: {chat_url} (jump to Qianliu AI homepage)'


class OpenAppConstant:
    """Open application"""
    APPROVAL = 'approval'  # Under approval
    APPROVED = 'approved'  # Approved
    FAIL = 'fail'  # Approval failed
    DISABLE = 'disable'  # Disabled
    EXPIRED = 'expired'  # Expired
    STATE_CHOICES = (
        (APPROVAL, 'Under approval'),
        (APPROVED, 'Approved'),
        (FAIL, 'Approval failed'),
        (DISABLE, 'Disabled'),
        (EXPIRED, 'Expired'),
    )
    ALLOW_DELETE_STATES = (FAIL, DISABLE, EXPIRED)  # States allowed to be deleted
    ALLOW_NOTICE_STATES = (APPROVED, FAIL, DISABLE)  # States allowed to be notified
    APPROVE_REMARK_NOT_EMPTY_STATES = (FAIL, DISABLE)  # States where approval remarks are required
    SQUARE_RETURN_STATES = (APPROVED, DISABLE, EXPIRED)  # States where square data can be returned


class UserConstant:
    CACHE_KEY_API_KEY = "users:api_key"
    CACHE_KEY_ID = "users:id"
    CACHE_KEY_USERNAME = "users:username"
    # Set of user avatar background colors
    AVATAR_COLORS = ['#4179FF', '#3AC8FF', '#8439FF', '#E251F5', '#49F4BA', '#A2E40B', '#FFC800', '#FF8000', '#F55151',
                     '#FF5FA0']


class ApiRuleConstant:
    """api rules/permissions"""
    DEPT = 'dept'
    USER = 'user'
    RULE_TYPE_CHOICES = (
        (DEPT, 'Department'),
        (USER, 'User'),
    )
    ALLOW_COMPANY = '深信服科技股份有限公司'


class AnalysisConstant:
    CACHE_KEY_WORK_ID = 'Analysis:work_id'
    CACHE_KEY_DEPT_LIST = 'dept_list'


class ConfigurationConstant:
    CACHE_KEY_PREFIX = "configuration"
    PROMPT_TYPE = 'prompt'
    PROMPT_KEY_FORBID_STRING = 'forbidden_word'
    PROMPT_RE_MAX_LENGTH = 5000
    AD_ON = 'on'
    LANGUAGE_TYPE = 'language'
    LANGUAGE_KEY_MAP = 'language_map'
    CACHE_KEY_LANGUAGE_MAP = 'language_map'
    CACHE_TYPE_IDE_CONFIG = 'ide_config'

    REVIEW_TYPE = 'review'

    # prompt template Other actions have configurations
    PROMPT_TEMPLATE = 'prompt_template'
    # Other templates
    MANUAL_REVIEW_PROMPT = 'manual_review'
    # Continuation writing template
    CONTINUE_PROMPT = 'continue'

    # Permissions
    PERMISSION_TYPE = 'permission'

    # System configuration items
    SYSTEM_TYPE = 'system_config'
    SYSTEM_KEY = 'front_end'  # Front-end common

    # Model control value settings
    MODEL_BELONG_TYPE = "model"
    ENABLED_MODELS = "enable_models"

    # Context control value settings
    CONTEXT_BELONG_TYPE = "context"
    CONTEXT_MAX_NUM = "context_max_num"


class PromptConstant:
    CACHE_KEY_FORBID_WORD = 'prompt_forbidden_word'
    CHECK_PARAM_LIST = ['prompt', 'code', 'custom_instructions', 'system_prompt']  # Parameters that need to be checked for sensitive words
    FORBID_WORD_RETURN_MESSAGE = 'According to safety regulations, the question words are not allowed to contain company names, passwords, etc. Please rephrase the question (the current question contains sensitive words: {})'
    OLD_PLUGIN_RETURN_MESSAGE = 'In order to provide better services and user experience, please upgrade to the latest version. After the upgrade is complete, restart the IDE. Configuration connection: http://docs.sangfor.org/x/rNnHDw '
    TOKENS_OVER_LENGTH = 'Your question exceeds the maximum number of tokens limit, please shorten the question and try again.'
    PLUGIN_LABELS = ['node-fetch', 'qianliu-ai-jetbrains-plugin']
    DEVOPS_LABELS = ['cicd service', 'qianliu-devops', 'tp service']
    RESPONSE_TEMPLATE = {
        'choices': [
            {
                'finish_reason': 'stop',
                'index': 0,
                'message': {
                    'content': 'Answer the question',
                    'role': 'assistant'
                }
            }
        ],
        'created': '1722650508',  # Need to reassign the current time.time()
        'id': 'chatcmpl-72bxP8TakrdRMN4Ln2b1VQrV2VpKJ',  # Reassign as needed
        'model': None,  # Need to specify the corresponding model
        'object': 'chat.completion',
        'usage': {
            'completion_tokens': 34,
            'prompt_tokens': 50,
            'total_tokens': 84
        }
    }
    # Sensitive word replacement mapping table (using regular replacement), the key is the replaced character, and the value is the sensitive word
    FORBIDDEN_WORD_MAP = {
        '_hello_': 'sangfor|sinfor|sangfor123|admin123|sangfor@123|Sangfor@123|sangforos',
        '_深圳_': '深信服|信服'
    }

    # Sensitive word replacement mapping table one-to-one (all are city words)
    SENSITIVE_WORD_MAP = {
        'Sangfor@123': 'Philadelphia',
        'sangfor@123': 'Colorado',
        'sangfor123': 'Pakistan',
        'sangforos': 'Illinois',
        'sangfor': 'Manchester',
        'sinfor': 'Alexander',
        'admin123': 'Hamilton',
        '深信服': 'Malaysia',
        '信服': 'Barcelona',
    }
    TARGET_WORD_MAP = {v: k for k, v in SENSITIVE_WORD_MAP.items()}


class ADConstant:
    CACHE_KEY_QIANLIU_AD = 'qianliu_ad'  # Qianliu advertising configuration cache key
    CACHE_PREFIX_KEY = "AD"  # User advertising cache prefix key
    CACHE_TIMEOUT = 60 * 60 * 24 * 30  # Each user is exposed to an advertisement once per month


class AIReviewConstant:
    TOKENIZER_PATH = 'runtime/tokenizer.json'
    MAX_TOKEN = 2048
    TREE_SITTER_LIB_PATH = 'runtime/languages.so'
    MAX_REVIEW_NUM = 5  # Maximum number of reviews for a single file (excluding those with prompt exceeding tokens, direct reuse of results, the actual number of reviews required)
    STREAM_SEPARATOR = '#data_id#'

    class ReviewType:
        AUTO = 'auto'  # Automatic
        MANUAL = 'manual'  # Manual
        CHOICES = (
            (AUTO, 'Automatic'),
            (MANUAL, 'Manual'),
        )

    class ReviewState:
        INIT = 'init'  # Initial
        SUCCESS = 'success'  # Success
        FAIL = 'fail'  # Fail
        CHOICES = (
            (INIT, 'Initial'),
            (SUCCESS, 'Success'),
            (FAIL, 'Fail')
        )

    class Flag:
        REPAIR = 'repair'  # Marked as resolved
        NO_REPAIR = 'no_repair'  # Marked as not repaired
        REJECT = 'reject'  # Reject this issue

        SKIP_REVIEW = (NO_REPAIR, REJECT)  # Skip
        REUSE_REVIEW = ('', REPAIR)  # Reuse

        CHOICES = (
            (REPAIR, 'Marked as resolved'),
            (NO_REPAIR, 'Marked as not repaired'),
            (REJECT, 'Reject this issue'),
        )

    TREE_SITTER_CODE_TYPE_MAP = {
        'vue': ['method_definition'],
        'javascript': ['method_definition', 'function_declaration'],
        'typescript': ['method_definition', 'function_declaration'],
        'python': ['function_definition'],
        'go': ['function_declaration'],
        'c': ['function_definition'],
        'bash': ['function_definition'],
        'lua': ['function_definition_statement'],
        'java': ['method_declaration'],
        'php': ['function_definition', 'method_declaration'],
        'ruby': ['method', 'singleton_method']
    }


class AskStreamConfig:
    # Too few loop iterations can easily lead to false positives, so increase it a bit
    LOOP_COUNT_LIMIT = 30


class CodeCompletionConstant:
    allow_departments = 'allow_department'


class ScribeConstant:
    ES_ID_TITLE = "dmsc"
    RESPONSE_TEMPLATE = {
        "success": False,
        "message": 'I am a question answering artificial intelligence, can access the Internet and answer questions in Chinese markdown format.',
        "data": None
    }
    # System presets for generating code by selecting words
    SCRIBE_SYSTEMS = [
        """You are an experienced development engineer.
        Your task is to implement code that meets the requirements,
        and the result needs to be compared with the selected code for diff differences,
        so you need to make sure that you do not omitted code for brevity,
        and finally, use the markdown format in output"""]
    # Intermediate processing type
    ADD_TAG = 'add_tag'
    VECTOR_RECALL = 'vector_recall'
    BASIC_SAFEGUARD = 'basic_safeguard'
    FILTER_DESC = 'filter_desc'
    FILTER_API = 'filter_api_docs'
    GENERATE_CODE = 'generate_code'
    MERGE_CODE = 'merge_code'
    keyword_dict = {"表格": "表格", "表单": "表单", "详情列": "多列详情列"}
    # Languages allowed for front-end specified component libraries
    CUSTOM_COMPONENT_ALLOW_LANGUAGES = ['javascript', 'typescript', 'html', 'vue']
    # Regular expressions for components in each document
    component_patterns = [
        r'(?<![A-Za-z\u4e00-\u9fa5])<([a-zA-Z0-9-]+)',  # Matches component names
        r'import .*?\{([^\}]+)\} from',  # Matches imports with {}
        r'import (\w+[\s,]*\w*)+ from'  # Matches imports without {}
    ]
    exclude_component_list = ["a", "div", "template", "style", "script", "p", "img", "span", "i", "section", "h2", "h1"]


class CheckApiParamsType:
    """
    # Verify parameter information method in api_info
    """
    # 1. close: do not verify; 2. request: only verify incoming parameters; 3. all: verify both incoming and outgoing parameters
    CLOSE = "close"
    REQUEST = "request"
    ALL = "all"

class AgentConstant:
    TASK_CHAT_QUEUE = "task_chat_queue"
    CELERY_TASK_TIMEOUT = 60 * 60  # Task execution timeout time, 1h

    CACHE_KEY_ZHUGE_ADS = "CACHE_KEY_ZHUGE_ADS"  # Qianliu Zhuge page recommended word list cache key
    """
    [{
        "title": "",         # Title displayed on the homepage
        "prompt": "",        # Specific prompt words (content displayed after clicking the panel), if it does not exist, take the title as the prompt word
        "use_agent": true    # Whether to enable intelligent team
    }]
    """

    AGENT_CHAT_DONE_MSG = "[DONE]"

    ROLE_OBSERVER = 'observer'  # Intelligent team observer role
    ROLE_GROUP_MEMBER = 'group_member'  # Intelligent team member
    ROLE_GROUP_GUARDIAN = 'group_guardian'  # Intelligent team guardian, fallback role
    ROLE_NORMAL_CHAT = 'normal_chat'  # Normal chat role

    AGENT_THOUGHT_EVENT = "dify_agent_thought"
    AGENT_ADVISE_EVENT = "agent_advise"
    AGENT_START_EVENT = "agent_start"
    AGENT_END_EVENT = "agent_end"

    ROLE_CHOICES = (
        (ROLE_OBSERVER, 'Observer'),
        (ROLE_GROUP_MEMBER, 'Group member'),
        (ROLE_NORMAL_CHAT, 'Normal chat')
    )

    # Agent's display extraction rules for the backend, such as getting names from historical conversations
    AGENT_DISPLAY_NAME_PATTERN = r'\|([^\|]*)'
    # Agent's display extraction rules for the front end
    AGENT_UI_PATTERN = r'^(.*?)\|'


class LoggerNameContant:
    SOCKET_SERVER = "socket_server"
    SIO = "socketio"


class ContextNavigationConstant:
    # redis cache key of context
    code_navigation_context_redis_key = "cnc-{uuid}"
    get_local_context_redis_key = "glc-{uuid}"
    cnc_redis_ex_time = 60 * 60  # Cache time 1 hour

    # dynamic context key
    get_file_content_action = "get_file_content"
    get_file_sign_action = "get_file_sign"
    get_sign_contents_action = "get_sign_contents"

class ConversationRole:
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
