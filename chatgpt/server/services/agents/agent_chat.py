import json

from autogen.io.base import IOStream

from services.action import get_action_strategy, ChatbotOptions
from bot.chat_history import get_history
from services.agents.agent_data_classes import ChatRequestData, make_cls_with_dict
from logger import get_task_chat_logger


class AgentChatBot:
    """
    单角色对话
    """
    def __init__(self, conv_id, chat_id, history=None):
        super().__init__()
        # 本轮对话
        self.conv_id = conv_id
        # 本次对话
        self.chat_id = chat_id
        # 对话历史管理器
        self.history = history if history else get_history()
        self.logger = get_task_chat_logger()

    def chat_stream(self, req: ChatRequestData, username=None):
        """
        流式对话，单角色对话
        """
        self.history.load_conversation(self.conv_id)
        self._chat_normal(req, username=username)
        self.history.save_conversation(self.conv_id)

    def _get_advise(self, req: ChatRequestData, username=None):
        """
        获取LLM建议的下一步操作列表，该操作是针对本轮对话的后续常见操作
        """
        iostream = IOStream.get_default()
        data = {
            "username": username,
            "display_name": username,
            "conversation_id": self.conv_id,
            "chat_id": self.chat_id,
            "language": req.language,
            "prompt": req.prompt,
            "query": req.query,
            "code": req.code,
            "action": "advise"
        }
        data = make_cls_with_dict(ChatRequestData, data)
        options = ChatbotOptions()
        options.stream = True
        strategy = get_action_strategy(data.action)
        strategy.set_history(self.history)
        strategy.set_logger(self.logger)
        data.prompt = strategy.get_prompt(req)
        result = strategy.make_result(data, options)
        self.logger.info(f"_get_advise(): result: {result}")
        try:
            index = result.find('[')
            if index != -1:
                result = result[index:]     # 包含 '[' 及其后面的内容
            index = result.rfind(']')
            if index != -1:
                result = result[:index + 1]  # 提取 '[' 到 ']' 之间的内容
            data = json.loads(result)
            iostream.print_agent_advise(data)
        except json.decoder.JSONDecodeError:
            self.logger.error(f"_get_advise() error: result: {result}")
            iostream.print_agent_advise([{
                    "title": "输出更多选择", "prompt": "输出更多可选方案"
                }, {
                    "title": "推荐最佳方案", "prompt": "推荐一个最佳方案"
                }])

    def _chat_normal(self, req: ChatRequestData, username=None):
        """
        普通对话，无代码上下文

        Args:
            query (str): 用户输入的查询。
            username (optional): 当前用户信息。
        Returns:
            None
        """
        iostream = IOStream.get_default()

        data = {
            "username": username,
            "display_name": username,
            "conversation_id": self.conv_id,
            "chat_id": self.chat_id,
            "language": req.language,
            "prompt": req.prompt,
            "query": req.query,
            "code": req.code,
            "action": "zhuge_normal_chat"
        }
        data = make_cls_with_dict(ChatRequestData, data)
        options = ChatbotOptions()
        options.stream = True
        strategy = get_action_strategy(data.action)
        strategy.set_history(self.history)
        strategy.set_logger(self.logger)
        data.prompt = strategy.get_prompt(req)
        full_data = ""
        for chunk_data in strategy.make_result(data, options):
            if chunk_data:
                if chunk_data.get("event", "") == "sf_tokens":
                    full_data = chunk_data.get("total_answer", "")
                iostream.print_chunk(
                    chunk_data,
                    sender="诸葛神码",
                    sender_icon=None
                )
        self._get_advise(req, username)
        # 为保障后续的一问一答的正常运行，在这里构造历史完整会话流
        self.history.add_user_message(req.prompt)
        self.history.add_ai_message(full_data)

