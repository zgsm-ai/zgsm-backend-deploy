import json

from autogen.io.base import IOStream

from services.action import get_action_strategy, ChatbotOptions
from bot.chat_history import get_history
from services.agents.agent_data_classes import ChatRequestData, make_cls_with_dict
from logger import get_task_chat_logger


class AgentChatBot:
    """
    Single role conversation
    """
    def __init__(self, conv_id, chat_id, history=None):
        super().__init__()
        # Current round of conversation
        self.conv_id = conv_id
        # This conversation
        self.chat_id = chat_id
        # Conversation history manager
        self.history = history if history else get_history()
        self.logger = get_task_chat_logger()

    def chat_stream(self, req: ChatRequestData, username=None):
        """
        Streaming conversation, single role conversation
        """
        self.history.load_conversation(self.conv_id)
        self._chat_normal(req, username=username)
        self.history.save_conversation(self.conv_id)

    def _get_advise(self, req: ChatRequestData, username=None):
        """
        Get the next step operation list suggested by LLM, which is a common follow-up operation for this round of conversation
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
                result = result[index:]     # Contains '[' and the content after it
            index = result.rfind(']')
            if index != -1:
                result = result[:index + 1]  # Extract the content between '[' and ']'
            data = json.loads(result)
            iostream.print_agent_advise(data)
        except json.decoder.JSONDecodeError:
            self.logger.error(f"_get_advise() error: result: {result}")
            iostream.print_agent_advise([{
                    "title": "Output more options", "prompt": "Output more alternative solutions"
                }, {
                    "title": "Recommend the best solution", "prompt": "Recommend the best solution"
                }])

    def _chat_normal(self, req: ChatRequestData, username=None):
        """
        Normal conversation, no code context

        Args:
            query (str): User input query.
            username (optional): Current user information.
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
                    sender="Zhuge Shenma",
                    sender_icon=None
                )
        self._get_advise(req, username)
        # In order to ensure the normal operation of the subsequent Q&A, construct a complete historical conversation stream here
        self.history.add_user_message(req.prompt)
        self.history.add_ai_message(full_data)
