from bot.conversation import Conversation
from bot.cache import get_redis
from config import conf

class ChatHistory:
    """
    Chatbot with conversation history and context information
    """
    def __init__(self, redis = None) -> None:
        # TODO: Consider changing to a persistent storage form of the database later
        if redis is None:
            redis = get_redis(conf)
        self.conv_db = Conversation(redis)
        self.chat_history = []

    def add_qa(self, 
        query: str, 
        answer: str, 
        conv_id: str, 
        user_name: str = 'user', 
        ai_name: str = 'assistant', 
        context_association: bool = True
    ) -> None:
        """
        Add a question and answer to the chat history
        """
        self.add_user_message(query, user_name=user_name)
        self.add_ai_message(answer, ai_name=ai_name)
        if conv_id and context_association:
            self.save_conversation(conv_id)

    def add_ai_message(self, message: str, ai_name: str = "assistant") -> bool:
        return self._add_message(message, ai_name)

    def add_user_message(self, message: str, user_name: str = "user") -> bool:
        return self._add_message(message, user_name)

    def _add_message(self, message: str, role_name: str) -> bool:
        self.chat_history.append({
            "role": role_name,
            "content": message
        })
        return True

    def make_conversation(self, conversation_id: str) -> None:
        """
        Make a conversation
        """
        self.conv_db.add_conversation(conversation_id, [])

    def rollback(self, num: int) -> None:
        """
        Rollback chat history num times
        """
        for _ in range(num):
            self.chat_history.pop()

    def reset(self) -> None:
        """
        Reset chat history
        """
        self.chat_history = []

    def load_conversation(self, conversation_id) -> None:
        """
        Load a conversation from the conversation history
        """
        if not self.conv_db.is_exist(conversation_id):
            # Create a new conversation
            self.make_conversation(conversation_id)
        self.chat_history = self.conv_db.get_conversation(conversation_id)

    def save_conversation(self, conversation_id) -> None:
        """
        Save a conversation to the conversation history
        """
        self.conv_db.add_conversation(conversation_id, self.chat_history)

# Default conversation history manager
default_history = None

def get_history():
    global default_history
    if default_history is None:
        default_history = ChatHistory(get_redis(conf))
    return default_history
