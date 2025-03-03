#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    项目常量

    :作者: 苏德利 16646
    :时间: 2023/3/3 15:31
    :修改者: 刘鹏 z10807
    :更新时间: 2023/4/21 9:26
"""


class ActionsConstant:
    FIND_BUGS = "findProblems"
    ADD_TEST = "addTests"
    OPTIMIZE = "optimize"
    EXPLAIN = "explain"
    CHAT = "chat"
    ADVISE="advise"
    GENERATE_CODE = "generateCode"
    # e2e 用例生成========
    REVIEW = "review"
    SCRIBE = "scribe"
    ADD_DEBUG_CODE = "addDebugCode"  # 添加调试代码
    ADD_STRONGER_CODE = "addStrongerCode"  # 添加健壮性代码
    ADD_COMMENT = "addComment"  # 添加注释
    PICK_COMMON_FUNC = "pickCommonFunc"  # 公共函数提取
    SIMPLIFY_CODE = "simplifyCode"  # 精简代码
    GIVE_ADVICE = "giveAdvice"  # 给出建议
    CONTINUE = "continue"  # 续写
    ZHUGE_NORMALCHAT = 'zhuge_normal_chat'  # 诸葛普通聊天

class GPTModelConstant:
    GPT_35 = "gpt-3.5"  # 使用 GPT_35_16K ，仅在请求参数中使用
    GPT_TURBO = "gpt-3.5-turbo"  # 使用 GPT_35_16K ，仅在请求参数中使用
    GPT_35_16K = "gpt-35-turbo-16k"  # 16k模型
    GPT_4 = "gpt-4"  # 128k模型
    GPT_4o = "gpt-4o"  # 128k模型
    GPT_35_CHAT_MODELS = [GPT_TURBO, GPT_35_16K]  # 支持模型列表
    DEEPSEEK_SEEK_CHAT = "deepseek-chat"
    CHAT_MODELS = [GPT_TURBO, GPT_35_16K, GPT_4, GPT_4o, DEEPSEEK_SEEK_CHAT, ]  # 支持模型列表


class GPTConstant:
    TIMEOUT = 120  # 单位: s
    GPT35_16K_MAX_TOKENS = 12000  # 输入上限12k
    GPT4_MAX_TOKENS = 60000  # 输入上限60k
    DEEPSEEK_SEEK_CHAT_TOKENS = 128000
    # 代码生成限制最大 token 数，要比最大 token 数小。
    CODE_GENERATE_MAX_PROMPT_TOKENS = GPT35_16K_MAX_TOKENS - 200

    # 响应格式类型
    RESPONSE_JSON_OBJECT = 'json_object'
    RESPONSE_FORMAT_TYPES = [RESPONSE_JSON_OBJECT]  # gpt新版支持返回格式类型列表

    SCRIBE_MAX_PROMPT_TOKENS = 6000  # 划词对话限制最大tokens

    MAX_CONTINUE_COUNT = 2  # 允许最大续写次数
    CONTINUE_SIGN = '\n----------续写----------\n'  # 续写标识
    # 允许自动续写actions
    ALLOW_CONTINUE_ACTIONS = [
        ActionsConstant.CONTINUE,
        ActionsConstant.SCRIBE,
    ]

    # 完成原因
    class FinishReason:
        STOP = 'stop'  # API 返回了完整的模型输出。
        LENGTH = 'length'  # 由于 max_tokens 参数或标记限制，模型输出不完整。
        CONTENT_FILTER = 'content_filter'  # 由于内容筛选器的标志，省略了内容。
        NULL = 'null'  # API 回复仍在进行中或未完成。


class TikTokenEncodeType:
    CL100K_BASE = "cl100k_base"  # ChatGPT models, text-embedding-ada-002, include gpt-3.5-turbo
    P50K_BASE = "p50k_base"  # Code models, text-davinci-002, text-davinci-003
    R50K_BASE = "r50k_base"  # (or gpt2)	GPT-3 models like davinci


class ServeConstant:
    THREADS = 4  # waitress serve用于处理应用程序逻辑的线程数，默认为4。
    CONNECTION_LIMIT = 100
    DEFAULT_API_TYPE = "openai"


class NullValueSort:
    """
    将None值排序放在前或者后
    """
    NULL_FIRST = 'null_first'
    NULL_LAST = 'null_last'


class AppConstant:
    DELETED = True
    REQUESTS_TIMEOUT_TIME = [2, 4, 8, 16, 32, 64]
    DEPT_CACHE_TIMEOUT = 86400  # 部门数据缓存24小时


class UserRole:
    ADMIN = "admin"  # 管理员
    USER = "user"  # 普通用户


class ErrorMsgs:
    TIMEOUT = 'Cancelling nested steps due to timeout'  # 任务执行时间超出设定的时间，默认60分钟
    GITLAB_NOT_RESPONDE = 'GitLab is not responding'  # gitlab 502报错关键字段


class AdminNoticeContent:
    """管理员通知内容"""
    CONTENT = '千流AI通知：\n用户{username}申请API账号。\n请前往后台管理进行审批：{chat_admin_url}'


class ApplicantNoticeContent:
    """申请人通知内容"""
    CONTENT = '千流AI通知：\n{first_line}{approve_remark}\n应用名称：{project_name}\n到期时间：{expiration_time}\n' \
              '申请原因：{application_reason}\n预期收益：{expected_profit}\n' \
              '更多操作，可前往千流AI平台：{chat_url}（跳转到千流ai首页）'


class OpenAppConstant:
    """开放应用"""
    APPROVAL = 'approval'  # 审批中
    APPROVED = 'approved'  # 审批通过
    FAIL = 'fail'  # 审批未通过
    DISABLE = 'disable'  # 已禁用
    EXPIRED = 'expired'  # 已超期
    STATE_CHOICES = (
        (APPROVAL, '审批中'),
        (APPROVED, '审批通过'),
        (FAIL, '审批未通过'),
        (DISABLE, '已禁用'),
        (EXPIRED, '已超期'),
    )
    ALLOW_DELETE_STATES = (FAIL, DISABLE, EXPIRED)  # 允许删除的状态
    ALLOW_NOTICE_STATES = (APPROVED, FAIL, DISABLE)  # 允许通知的状态
    APPROVE_REMARK_NOT_EMPTY_STATES = (FAIL, DISABLE)  # 审批备注必填的状态
    SQUARE_RETURN_STATES = (APPROVED, DISABLE, EXPIRED)  # 广场数据可返回的状态


class UserConstant:
    CACHE_KEY_API_KEY = "users:api_key"
    CACHE_KEY_ID = "users:id"
    CACHE_KEY_USERNAME = "users:username"
    # 用户头像背景色集合
    AVATAR_COLORS = ['#4179FF', '#3AC8FF', '#8439FF', '#E251F5', '#49F4BA', '#A2E40B', '#FFC800', '#FF8000', '#F55151',
                     '#FF5FA0']


class ApiRuleConstant:
    """api规则/权限"""
    DEPT = 'dept'
    USER = 'user'
    RULE_TYPE_CHOICES = (
        (DEPT, '部门'),
        (USER, '用户'),
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

    # prompt模板 其他每个action都有配置
    PROMPT_TEMPLATE = 'prompt_template'
    # 其他模板
    MANUAL_REVIEW_PROMPT = 'manual_review'
    # 续写模板
    CONTINUE_PROMPT = 'continue'

    # 权限
    PERMISSION_TYPE = 'permission'

    # 系统配置项
    SYSTEM_TYPE = 'system_config'
    SYSTEM_KEY = 'front_end'  # 前端通用

    # 模型控制值设置
    MODEL_BELONG_TYPE = "model"
    ENABLED_MODELS = "enable_models"

    # 上下文控制值设置
    CONTEXT_BELONG_TYPE = "context"
    CONTEXT_MAX_NUM = "context_max_num"


class PromptConstant:
    CACHE_KEY_FORBID_WORD = 'prompt_forbidden_word'
    CHECK_PARAM_LIST = ['prompt', 'code', 'custom_instructions', 'system_prompt']  # 需要校验敏感词的参数
    FORBID_WORD_RETURN_MESSAGE = '安全规定，提问词不允许包含 公司名称、密码等字样，请重新提问 （当前问题包含敏感词：{}）'
    OLD_PLUGIN_RETURN_MESSAGE = '为了提供更好的服务和用户体验，请升级到最新版本。升级完成之后，重启IDE即可。配置连接：http://docs.sangfor.org/x/rNnHDw '
    TOKENS_OVER_LENGTH = '您的提问超过了最大 token 数限制，请缩短提问后重试。'
    PLUGIN_LABELS = ['node-fetch', 'qianliu-ai-jetbrains-plugin']
    DEVOPS_LABELS = ['cicd service', 'qianliu-devops', 'tp service']
    RESPONSE_TEMPLATE = {
        'choices': [
            {
                'finish_reason': 'stop',
                'index': 0,
                'message': {
                    'content': '回答问题',
                    'role': 'assistant'
                }
            }
        ],
        'created': '1722650508',  # 需重新赋值当前 time.time()
        'id': 'chatcmpl-72bxP8TakrdRMN4Ln2b1VQrV2VpKJ',  # 根据需要重新赋值
        'model': None,  # 需指定对应model
        'object': 'chat.completion',
        'usage': {
            'completion_tokens': 34,
            'prompt_tokens': 50,
            'total_tokens': 84
        }
    }
    # 敏感词替换映射表（使用正则替换），键为替换后的字符，值为敏感词
    FORBIDDEN_WORD_MAP = {
        '_hello_': 'sangfor|sinfor|sangfor123|admin123|sangfor@123|Sangfor@123|sangforos',
        '_深圳_': '深信服|信服'
    }

    # 敏感词替换映射表 一对一 （皆为城市单词）
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
    CACHE_KEY_QIANLIU_AD = 'qianliu_ad'  # 千流广告配置缓存key
    CACHE_PREFIX_KEY = "AD"  # 用户广告缓存前缀key
    CACHE_TIMEOUT = 60 * 60 * 24 * 30  # 每个用户投放一次广告时间 1次/1月


class AIReviewConstant:
    TOKENIZER_PATH = 'runtime/tokenizer.json'
    MAX_TOKEN = 2048
    TREE_SITTER_LIB_PATH = 'runtime/languages.so'
    MAX_REVIEW_NUM = 5  # 单文件最多进行review数量（排除prompt超tokens的、直接复用结果的，实际需要请求review的数量）
    STREAM_SEPARATOR = '#data_id#'

    class ReviewType:
        AUTO = 'auto'  # 自动
        MANUAL = 'manual'  # 手动
        CHOICES = (
            (AUTO, '自动'),
            (MANUAL, '主动'),
        )

    class ReviewState:
        INIT = 'init'  # 初始
        SUCCESS = 'success'  # 成功
        FAIL = 'fail'  # 失败
        CHOICES = (
            (INIT, '初始'),
            (SUCCESS, '成功'),
            (FAIL, '失败')
        )

    class Flag:
        REPAIR = 'repair'  # 标记为解决
        NO_REPAIR = 'no_repair'  # 标记为不修复
        REJECT = 'reject'  # 拒绝此问题

        SKIP_REVIEW = (NO_REPAIR, REJECT)  # 跳过
        REUSE_REVIEW = ('', REPAIR)  # 复用

        CHOICES = (
            (REPAIR, '标记为解决'),
            (NO_REPAIR, '标记为不修复'),
            (REJECT, '拒绝此问题'),
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
    # 循环次数太少容易误杀，提高一点
    LOOP_COUNT_LIMIT = 30


class CodeCompletionConstant:
    allow_departments = 'allow_department'


class ScribeConstant:
    ES_ID_TITLE = "dmsc"
    RESPONSE_TEMPLATE = {
        "success": False,
        "message": '我是一个问题回答人工智能，可以访问互联网并以中文 markdown 格式回答问题。',
        "data": None
    }
    # 划词生成代码的系统预设
    SCRIBE_SYSTEMS = [
        """You are an experienced development engineer.
        Your task is to implement code that meets the requirements,
        and the result needs to be compared with the selected code for diff differences,
        so you need to make sure that you do not omitted code for brevity,
        and finally, use the markdown format in output"""]
    # 中间处理类型
    ADD_TAG = 'add_tag'
    VECTOR_RECALL = 'vector_recall'
    BASIC_SAFEGUARD = 'basic_safeguard'
    FILTER_DESC = 'filter_desc'
    FILTER_API = 'filter_api_docs'
    GENERATE_CODE = 'generate_code'
    MERGE_CODE = 'merge_code'
    keyword_dict = {"表格": "表格", "表单": "表单", "详情列": "多列详情列"}
    # 允许前端指定组件库的语言
    CUSTOM_COMPONENT_ALLOW_LANGUAGES = ['javascript', 'typescript', 'html', 'vue']
    # 各文档中组件的正则表达式
    component_patterns = [
        r'(?<![A-Za-z\u4e00-\u9fa5])<([a-zA-Z0-9-]+)',  # 匹配组件名
        r'import .*?\{([^\}]+)\} from',  # 匹配带{}的导入的hook
        r'import (\w+[\s,]*\w*)+ from'  # 匹配不带{}的导入的hook
    ]
    exclude_component_list = ["a", "div", "template", "style", "script", "p", "img", "span", "i", "section", "h2", "h1"]


class CheckApiParamsType:
    """
    # 校验api_info中参数信息方式
    """
    # 1、close不校验；2、request仅校验入参；3、all校验入参和出参
    CLOSE = "close"
    REQUEST = "request"
    ALL = "all"

class AgentConstant:
    TASK_CHAT_QUEUE = "task_chat_queue"
    CELERY_TASK_TIMEOUT = 60 * 60  # 任务执行超时时间，1h

    CACHE_KEY_ZHUGE_ADS = "CACHE_KEY_ZHUGE_ADS"  # 千流诸葛页面推荐词列表缓存key
    """
    [{
        "title": "",         # 首页展示标题
        "prompt": "",        # 具体提示词(点击后面板展示的内容),若不存在则取 title 为提示词
        "use_agent": true    # 是否启用智能团
    }]
    """

    AGENT_CHAT_DONE_MSG = "[DONE]"

    ROLE_OBSERVER = 'observer'  # 智能团观察者角色
    ROLE_GROUP_MEMBER = 'group_member'  # 智能团团员
    ROLE_GROUP_GUARDIAN = 'group_guardian'  # 智能团守卫者，兜底角色
    ROLE_NORMAL_CHAT = 'normal_chat'  # 普通聊天角色

    AGENT_THOUGHT_EVENT = "dify_agent_thought"
    AGENT_ADVISE_EVENT = "agent_advise"
    AGENT_START_EVENT = "agent_start"
    AGENT_END_EVENT = "agent_end"

    ROLE_CHOICES = (
        (ROLE_OBSERVER, '观察者'),
        (ROLE_GROUP_MEMBER, '群成员'),
        (ROLE_NORMAL_CHAT, '普通聊天')
    )

    # agent的服务于后台的展示提取规则，比如：历史会话里的名字获取
    AGENT_DISPLAY_NAME_PATTERN = r'\|([^\|]*)'
    # agent的服务于前端的展示提取规则
    AGENT_UI_PATTERN = r'^(.*?)\|'


class LoggerNameContant:
    SOCKET_SERVER = "socket_server"
    SIO = "socketio"


class ContextNavigationConstant:
    # context的redis缓存key
    code_navigation_context_redis_key = "cnc-{uuid}"
    get_local_context_redis_key = "glc-{uuid}"
    cnc_redis_ex_time = 60 * 60  # 缓存时间 1小时

    # 动态上下文的key
    get_file_content_action = "get_file_content"
    get_file_sign_action = "get_file_sign"
    get_sign_contents_action = "get_sign_contents"

class ConversationRole:
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
