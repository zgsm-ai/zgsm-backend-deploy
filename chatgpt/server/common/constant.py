#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Project Constants
"""


class ActionsConstant:
    FIND_BUGS = "findProblems"
    ADD_TEST = "addTests"
    OPTIMIZE = "optimize"
    EXPLAIN = "explain"
    CHAT = "chat"
    ADVISE="advise"
    GENERATE_CODE = "generateCode"
    # e2e test generation========
    REVIEW = "review"
    SCRIBE = "scribe"
    ADD_DEBUG_CODE = "addDebugCode"  # Add debug code
    ADD_STRONGER_CODE = "addStrongerCode"  # Add robust code
    ADD_COMMENT = "addComment"  # Add comments
    PICK_COMMON_FUNC = "pickCommonFunc"  # Extract common functions
    SIMPLIFY_CODE = "simplifyCode"  # Simplify code
    GIVE_ADVICE = "giveAdvice"  # Give advice
    CONTINUE = "continue"  # Continue writing
    SHENMA_NORMALCHAT = 'shenma_normal_chat'  # Shenma normal chat

class GPTModelConstant:
    GPT_35 = "gpt-3.5"  # Use GPT_35_16K, only used in request parameters
    GPT_TURBO = "gpt-3.5-turbo"  # Use GPT_35_16K, only used in request parameters
    GPT_35_16K = "gpt-35-turbo-16k"  # 16k model
    GPT_4 = "gpt-4"  # 128k model
    GPT_4o = "gpt-4o"  # 128k model
    GPT_35_CHAT_MODELS = [GPT_TURBO, GPT_35_16K]  # Supported model list
    DEEPSEEK_SEEK_CHAT = "deepseek-chat"
    CHAT_MODELS = [GPT_TURBO, GPT_35_16K, GPT_4, GPT_4o, DEEPSEEK_SEEK_CHAT, ]  # Supported model list


class GPTConstant:
    TIMEOUT = 120  # Unit: s
    GPT35_16K_MAX_TOKENS = 12000  # Input limit 12k
    GPT4_MAX_TOKENS = 60000  # Input limit 60k
    DEEPSEEK_SEEK_CHAT_TOKENS = 128000
    # Code generation maximum token limit, should be less than the maximum token count.
    CODE_GENERATE_MAX_PROMPT_TOKENS = GPT35_16K_MAX_TOKENS - 200

    # Response format types
    RESPONSE_JSON_OBJECT = 'json_object'
    RESPONSE_FORMAT_TYPES = [RESPONSE_JSON_OBJECT]  # List of supported return format types for new GPT version

    SCRIBE_MAX_PROMPT_TOKENS = 6000  # Maximum tokens limit for highlighted text conversation

    MAX_CONTINUE_COUNT = 2  # Maximum allowed continuation count
    CONTINUE_SIGN = '\n----------Continue----------\n'  # Continuation identifier
    # Actions that allow automatic continuation
    ALLOW_CONTINUE_ACTIONS = [
        ActionsConstant.CONTINUE,
        ActionsConstant.SCRIBE,
    ]

    # Completion reason
    class FinishReason:
        STOP = 'stop'  # The API returned the complete model output.
        LENGTH = 'length'  # The model output is incomplete due to the max_tokens parameter or token limit.
        CONTENT_FILTER = 'content_filter'  # Content was omitted due to content filter flags.
        NULL = 'null'  # The API response is still in progress or incomplete.


class TikTokenEncodeType:
    CL100K_BASE = "cl100k_base"  # ChatGPT models, text-embedding-ada-002, include gpt-3.5-turbo
    P50K_BASE = "p50k_base"  # Code models, text-davinci-002, text-davinci-003
    R50K_BASE = "r50k_base"  # (or gpt2)	GPT-3 models like davinci


class ServeConstant:
    THREADS = 4  # Number of threads used to process application logic for waitress serve, default is 4.
    CONNECTION_LIMIT = 100
    DEFAULT_API_TYPE = "openai"


class NullValueSort:
    """
    Sort NULL values to be placed at the beginning or end
    """
    NULL_FIRST = 'null_first'
    NULL_LAST = 'null_last'


class AppConstant:
    DELETED = True
    REQUESTS_TIMEOUT_TIME = [2, 4, 8, 16, 32, 64]
    DEPT_CACHE_TIMEOUT = 86400  # Department data cache for 24 hours


class UserRole:
    ADMIN = "admin"  # Administrator
    USER = "user"  # Regular user


class ErrorMsgs:
    TIMEOUT = 'Cancelling nested steps due to timeout'  # Task execution time exceeds the set time, default 60 minutes
    GITLAB_NOT_RESPONDE = 'GitLab is not responding'  # GitLab 502 error key field


class AdminNoticeContent:
    """Admin notification content"""
    CONTENT = 'Qianliu AI Notice:\nUser {username} is applying for an API account.\nPlease go to the admin panel for approval: {chat_admin_url}'


class ApplicantNoticeContent:
    """Applicant notification content"""
    CONTENT = 'Qianliu AI Notice:\n{first_line}{approve_remark}\nApplication Name: {project_name}\nExpiration Time: {expiration_time}\n' \
              'Application Reason: {application_reason}\nExpected Benefits: {expected_profit}\n' \
              'For more operations, please visit the Qianliu AI platform: {chat_url} (redirects to Qianliu AI homepage)'


class OpenAppConstant:
    """Open application"""
    APPROVAL = 'approval'  # In approval
    APPROVED = 'approved'  # Approved
    FAIL = 'fail'  # Not approved
    DISABLE = 'disable'  # Disabled
    EXPIRED = 'expired'  # Expired
    STATE_CHOICES = (
        (APPROVAL, 'In approval'),
        (APPROVED, 'Approved'),
        (FAIL, 'Not approved'),
        (DISABLE, 'Disabled'),
        (EXPIRED, 'Expired'),
    )
    ALLOW_DELETE_STATES = (FAIL, DISABLE, EXPIRED)  # States that allow deletion
    ALLOW_NOTICE_STATES = (APPROVED, FAIL, DISABLE)  # States that allow notification
    APPROVE_REMARK_NOT_EMPTY_STATES = (FAIL, DISABLE)  # States requiring approval remarks
    SQUARE_RETURN_STATES = (APPROVED, DISABLE, EXPIRED)  # States that can be returned in the marketplace data


class UserConstant:
    CACHE_KEY_API_KEY = "users:api_key"
    CACHE_KEY_ID = "users:id"
    CACHE_KEY_USERNAME = "users:username"
    # User avatar background color set
    AVATAR_COLORS = ['#4179FF', '#3AC8FF', '#8439FF', '#E251F5', '#49F4BA', '#A2E40B', '#FFC800', '#FF8000', '#F55151',
                     '#FF5FA0']


class ApiRuleConstant:
    """API rules/permissions"""
    DEPT = 'dept'
    USER = 'user'
    RULE_TYPE_CHOICES = (
        (DEPT, 'Department'),
        (USER, 'User'),
    )
    ALLOW_COMPANY = 'Sangfor Technologies Inc.'


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

    # Prompt templates, each action has its own configuration
    PROMPT_TEMPLATE = 'prompt_template'
    # Other templates
    MANUAL_REVIEW_PROMPT = 'manual_review'
    # Continuation template
    CONTINUE_PROMPT = 'continue'

    # Permissions
    PERMISSION_TYPE = 'permission'

    # System configuration items
    SYSTEM_TYPE = 'system_config'
    SYSTEM_KEY = 'front_end'  # Frontend common

    # Model control value settings
    MODEL_BELONG_TYPE = "model"
    ENABLED_MODELS = "enable_models"

    # Context control value settings
    CONTEXT_BELONG_TYPE = "context"
    CONTEXT_MAX_NUM = "context_max_num"


class PromptConstant:
    CACHE_KEY_FORBID_WORD = 'prompt_forbidden_word'
    CHECK_PARAM_LIST = ['prompt', 'code', 'custom_instructions', 'system_prompt']  # Parameters that need to be checked for sensitive words
    FORBID_WORD_RETURN_MESSAGE = 'For security reasons, questions are not allowed to contain company names, passwords, etc. Please ask again. (Current question contains sensitive words: {})'
    OLD_PLUGIN_RETURN_MESSAGE = 'To provide better service and user experience, please upgrade to the latest version. After upgrading, restart your IDE. Configuration link: http://docs.sangfor.org/x/rNnHDw '
    TOKENS_OVER_LENGTH = 'Your question exceeds the maximum token limit. Please shorten your question and try again.'
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
        'created': '1722650508',  # Need to reassign current time.time()
        'id': 'chatcmpl-72bxP8TakrdRMN4Ln2b1VQrV2VpKJ',  # Need to reassign according to needs
        'model': None,  # Need to specify corresponding model
        'object': 'chat.completion',
        'usage': {
            'completion_tokens': 34,
            'prompt_tokens': 50,
            'total_tokens': 84
        }
    }
    # Sensitive word replacement mapping table (using regex replacement), keys are replacement characters, values are sensitive words
    FORBIDDEN_WORD_MAP = {
        '_hello_': 'sangfor|sinfor|sangfor123|admin123|sangfor@123|Sangfor@123|sangforos',
        '_shenzhen_': 'sangfor|sinfor'
    }

    # Sensitive word one-to-one replacement mapping table (all are city words)
    SENSITIVE_WORD_MAP = {
        'Sangfor@123': 'Philadelphia',
        'sangfor@123': 'Colorado',
        'sangfor123': 'Pakistan',
        'sangforos': 'Illinois',
        'sangfor': 'Manchester',
        'sinfor': 'Alexander',
        'admin123': 'Hamilton',
        'sangfor': 'Malaysia',
        'sinfor': 'Barcelona',
    }
    TARGET_WORD_MAP = {v: k for k, v in SENSITIVE_WORD_MAP.items()}


class ADConstant:
    CACHE_KEY_QIANLIU_AD = 'qianliu_ad'  # Qianliu advertisement configuration cache key
    CACHE_PREFIX_KEY = "AD"  # User advertisement cache prefix key
    CACHE_TIMEOUT = 60 * 60 * 24 * 30  # Time for delivering an advertisement to each user once/month


class AIReviewConstant:
    TOKENIZER_PATH = 'runtime/tokenizer.json'
    MAX_TOKEN = 2048
    TREE_SITTER_LIB_PATH = 'runtime/languages.so'
    MAX_REVIEW_NUM = 5  # Maximum number of reviews for a single file (excluding those with prompt exceeding tokens and direct result reuse, actual number of review requests)
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
        FAIL = 'fail'  # Failure
        CHOICES = (
            (INIT, 'Initial'),
            (SUCCESS, 'Success'),
            (FAIL, 'Failure')
        )

    class Flag:
        REPAIR = 'repair'  # Mark as resolved
        NO_REPAIR = 'no_repair'  # Mark as not to be fixed
        REJECT = 'reject'  # Reject this issue

        SKIP_REVIEW = (NO_REPAIR, REJECT)  # Skip
        REUSE_REVIEW = ('', REPAIR)  # Reuse

        CHOICES = (
            (REPAIR, 'Mark as resolved'),
            (NO_REPAIR, 'Mark as not to be fixed'),
            (REJECT, 'Reject this issue'),
        )

    TREE_SITTER_CODE_TYPE_MAP = {
        # Map of file types to tree-sitter language identifiers
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
    # Too few loop count can lead to false positives, increase it a bit
    LOOP_COUNT_LIMIT = 30


class CodeCompletionConstant:
    allow_departments = 'allow_department'


class ScribeConstant:
    ES_ID_TITLE = "dmsc"
    RESPONSE_TEMPLATE = {
        "success": False,
        "message": 'I am a question-answering AI that can access the internet and respond in Chinese markdown format.',
        "data": None
    }
    # System preset for code generation with text selection
    SCRIBE_SYSTEMS = [
        """You are an experienced development engineer.
        Your task is to implement code that meets the requirements,
        and the result needs to be compared with the selected code for diff differences,
        so you need to make sure that you do not omitted code for brevity,
        and finally, use the markdown format in output"""]
    # Intermediate processing types
    ADD_TAG = 'add_tag'
    VECTOR_RECALL = 'vector_recall'
    BASIC_SAFEGUARD = 'basic_safeguard'
    FILTER_DESC = 'filter_desc'
    FILTER_API = 'filter_api_docs'
    GENERATE_CODE = 'generate_code'
    MERGE_CODE = 'merge_code'
    keyword_dict = {"table": "table", "form": "form", "detail column": "multi-column detail column"}
    # Languages that allow frontend to specify component libraries
    CUSTOM_COMPONENT_ALLOW_LANGUAGES = ['javascript', 'typescript', 'html', 'vue']
    # Regular expressions for components in various documents
    component_patterns = [
        r'(?<![A-Za-z\u4e00-\u9fa5])<([a-zA-Z0-9-]+)',  # Match component names
        r'import .*?\{([^\}]+)\} from',  # Match imported hooks with {}
        r'import (\w+[\s,]*\w*)+ from'  # Match imported hooks without {}
    ]
    exclude_component_list = ["a", "div", "template", "style", "script", "p", "img", "span", "i", "section", "h2", "h1"]


class CheckApiParamsType:
    """
    # Methods for verifying parameter information in api_info
    """
    # 1. close: no verification; 2. request: only verify input parameters; 3. all: verify both input and output parameters
    CLOSE = "close"
    REQUEST = "request"
    ALL = "all"


class AgentConstant:
    TASK_CHAT_QUEUE = "task_chat_queue"
    CELERY_TASK_TIMEOUT = 60 * 60  # Task execution timeout, 1h

    CACHE_KEY_SHENMA_ADS = "CACHE_KEY_SHENMA_ADS"  # Cache key for recommendation word list on Qianliu shenma page
    """
    [{
        "title": "",         # Title displayed on homepage
        "prompt": "",        # Specific prompt (content shown in panel after clicking), if not exists, use title as prompt
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
        (ROLE_GROUP_MEMBER, 'Group Member'),
        (ROLE_NORMAL_CHAT, 'Normal Chat')
    )

    # Rules for extracting agent display name for backend display, e.g., retrieving names from conversation history
    AGENT_DISPLAY_NAME_PATTERN = r'\|([^\|]*)'
    # Rules for extracting agent display for frontend UI
    AGENT_UI_PATTERN = r'^(.*?)\|'


class LoggerNameContant:
    SOCKET_SERVER = "socket_server"
    SIO = "socketio"


class ContextNavigationConstant:
    # Redis cache key for context
    code_navigation_context_redis_key = "cnc-{uuid}"
    get_local_context_redis_key = "glc-{uuid}"
    cnc_redis_ex_time = 60 * 60  # Cache time 1 hour

    # Keys for dynamic context
    get_file_content_action = "get_file_content"
    get_file_sign_action = "get_file_sign"
    get_sign_contents_action = "get_sign_contents"


class ConversationRole:
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
