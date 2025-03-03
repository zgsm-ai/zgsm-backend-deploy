from dataclasses import dataclass
from typing import Dict, List
from common.constant import GPTModelConstant, ActionsConstant
from datetime import datetime
import pytz

@dataclass
class ChatRequestData:
    # 动作：chat,addDebugCode,addCommentCode,explain etc.
    action: str = ActionsConstant.CHAT
    # programming language: c, cpp, python, java etc.
    language: str = ""
    # 注释语言
    comment_language: str = "Chinese"
    # 自定义指令集
    custom_instructions: str = None
    # 用户输入的查询信息
    query: str = None
    # 当前代码文件的路径
    path: str = ""
    # 根据用户请求构造的提示信息
    prompt: str = None
    # 对话模式: 单人对话或智能团对话
    mode: str = "normal"
    # 选中代码提问，未选中则为空
    code: str = ""
    # 本轮会话的唯一标识
    conversation_id: str = None
    # 本轮会话里的本次会话的唯一标识
    chat_id: str = None
    # 用户使用的客户端
    user_agent: str = ""
    # 用户所在的主机
    host: str = ""
    # 用户名
    username: str = ""
    # 用户邮箱
    email: str = ""
    # 用户显示名称
    display_name: str = ""
    # 请求创建时间
    created_at: str = ""
    # 请求结束时间
    finish_at: str = ""

    def __post_init__(self):
        """
        __post_init__ 方法会在 dataclass 的 __init__ 方法执行完毕后被调用
        """
        if not self.query:
            self.query = self.prompt
            if self.code:
                self.prompt = f"{self.query} \nSelected code:\n```\n{self.code}\n```"
        if not self.action:
            self.action = ActionsConstant.CHAT
        if not self.comment_language:
            self.comment_language = 'Chinese'
        if not self.created_at:
            self.created_at = datetime.now(pytz.timezone('Asia/Shanghai'))

    def to_dict(self):
        """
        把请求数据转成字典
        """
        return self.__dict__

def make_cls_with_dict(cls, dict_data):
    """
    根据字典内容构建一个数据对象，采用数据对象是为了保障数据的一致性，提升可读性
    """
    valid_datas = {}
    for key, value in dict_data.items():
        if hasattr(cls, key):
            valid_datas[key] = value
    result = cls(**valid_datas)
    if hasattr(cls, "raw_data"):
        result.raw_data = dict_data
    return result
