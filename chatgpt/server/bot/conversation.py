import json


class Conversation:
    """
    对话管理器: 可管理多轮对话
    注：对话数据缓存在redis中，借助redis，可以把整个诸葛神码服务的所有对话缓存起来，方便后续使用
    """

    def __init__(self, redis) -> None:
        self.cache = redis
        self.conversations = {}

    def add_conversation(self, key: str, history: list) -> None:
        """
        Adds a history list to the conversations dict with the id as the key
        """
        self.conversations[key] = history
        self.cache.set(key, history)
        self.cache.expire(key, 60 * 60)  # 缓存超时时间设置为1小时

    def get_conversation(self, key: str) -> list:
        """
        Retrieves the history list from the conversations dict with the id as the key
        """
        return self.cache.get(key)

    def remove_conversation(self, key: str) -> None:
        """
        Removes the history list from the conversations dict with the id as the key
        """
        del self.conversations[key]
        self.cache.remove(key)

    def is_exist(self, key: str):
        if key in self.cache.keys("*"):
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        Creates a JSON string of the conversations
        """
        return json.dumps(self.conversations)

    def save(self, file: str) -> None:
        """
        Saves the conversations to a JSON file
        """
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))

    def load(self, file: str) -> None:
        """
        Loads the conversations from a JSON file
        """
        with open(file, encoding="utf-8") as f:
            self.conversations = json.loads(f.read())
