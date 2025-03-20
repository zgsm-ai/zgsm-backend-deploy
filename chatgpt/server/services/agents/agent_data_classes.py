from dataclasses import dataclass
from typing import Dict, List
from common.constant import GPTModelConstant, ActionsConstant
from datetime import datetime
import pytz

@dataclass
class ChatRequestData:
    # Action: chat,addDebugCode,addCommentCode,explain etc.
    action: str = ActionsConstant.CHAT
    # programming language: c, cpp, python, java etc.
    language: str = ""
    # Comment language
    comment_language: str = "Chinese"
    # Custom instruction set
    custom_instructions: str = None
    # User input query information
    query: str = None
    # Path to the current code file
    path: str = ""
    # Prompt information constructed according to user requests
    prompt: str = None
    # Conversation mode: single person conversation or intelligent group conversation
    mode: str = "normal"
    # Select code to ask questions, empty if not selected
    code: str = ""
    # Unique identifier for this round of conversation
    conversation_id: str = None
    # Unique identifier for this conversation in this round of conversation
    chat_id: str = None
    # Client used by the user
    user_agent: str = ""
    # Host where the user is located
    host: str = ""
    # Username
    username: str = ""
    # User email
    email: str = ""
    # User display name
    display_name: str = ""
    # Request creation time
    created_at: str = ""
    # Request end time
    finish_at: str = ""

    def __post_init__(self):
        """
        The __post_init__ method is called after the __init__ method of the dataclass is executed
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
        Convert request data into a dictionary
        """
        return self.__dict__

def make_cls_with_dict(cls, dict_data):
    """
    Construct a data object based on dictionary content. The use of data objects is to ensure data consistency and improve readability
    """
    valid_datas = {}
    for key, value in dict_data.items():
        if hasattr(cls, key):
            valid_datas[key] = value
    result = cls(**valid_datas)
    if hasattr(cls, "raw_data"):
        result.raw_data = dict_data
    return result
