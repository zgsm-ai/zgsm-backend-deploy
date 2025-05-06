import json
import time
import traceback

from lib.cache import Cache
from common.constant import AgentConstant, ContextNavigationConstant
from third_platform.es.chat_messages.ide_data_as_service import ide_es_service
from autogen.io.base import IOStream
from services.agents.agent_chat import AgentChatBot
from services.agents.autogen_iostream import AgentChatIOStream
from .agent_data_classes import ChatRequestData

cache = Cache()


def ignore_exceptions(func):
    """
    Define function ignore_exceptions to decorate other functions to ignore all exceptions
    args:
        func: Function to be decorated
    return:
        wrapper function that catches and ignores exceptions
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return wrapper


class CursorObj:
    offset = 0


class DifyMessageQueueHelper:
    @classmethod
    def _push_data(cls, key, data):
        # Need to set timeout for the key; but the key can only be obtained during creation
        is_exist_key = True if cache.connection.exists(key) else False
        cache.connection.rpush(key, cache.serialize(data))
        if is_exist_key is True:
            # If the key doesn't exist, this is creating the key, so set an expiration time
            cache.connection.expire(key, 3600)

    @classmethod
    def _pop_data(cls, key):
        data = cache.connection.lpop(key)
        if not data:
            return data
        return cache.deserialize(data)

    @classmethod
    def _make_queue_key(cls, mq_id):
        return f"{AgentConstant.TASK_CHAT_QUEUE}:{mq_id}"

    @classmethod
    def push_json(cls, mq_id, json_data, cursor: CursorObj = None):
        if cursor:
            cursor.offset += 1
            json_data["offset"] = cursor.offset
        cls._push_data(cls._make_queue_key(mq_id), f"json:{json.dumps(json_data)}")

    @classmethod
    def push_msg(cls, mq_id, msg, cursor: CursorObj = None):
        if cursor:
            cursor.offset += 1
        cls._push_data(cls._make_queue_key(mq_id), f"msg:{msg}")

    @classmethod
    def handle_data(cls, data):
        if not data:
            return None
        if not isinstance(data, str):
            return data
        if data.startswith("json:"):
            json_data = json.loads(data[5:])
            return json_data
        elif data.startswith("msg:"):
            msg = data[4:]
            return msg

    @classmethod
    def pop_data(cls, mq_id):
        data = cls._pop_data(cls._make_queue_key(mq_id))
        return cls.handle_data(data)

    @classmethod
    def get_data_by_offset(cls, mq_id, offset):
        data = cache.connection.lindex(cls._make_queue_key(mq_id), offset)
        if data:
            return cls.handle_data(cache.deserialize(data))
        else:
            return data


class DifySpecifiedContextHelper(DifyMessageQueueHelper):
    """This class serves to retrieve context during the process; due to different business logic, it needs to reuse some queue methods"""

    @classmethod
    def _make_queue_key(cls, mq_id):
        redis_key = ContextNavigationConstant.get_local_context_redis_key.format(uuid=mq_id)
        return redis_key

    @classmethod
    def _blpop_data(cls, key, timeout=6) -> str:
        """
        Define class method _blpop_data to block-read data from cache
        args:
            key: Cache key
            timeout: Blocking timeout, default is 6 seconds
        return:
            Read data, if read times out, return default value "{}"
        """

        try:
            _, data = cache.connection.blpop(key, timeout)
            if data:
                return cache.deserialize(data)
        except TypeError:
            data = ""
            return data

    @classmethod
    def blpop_data(cls, mq_id):
        data = cls._blpop_data(cls._make_queue_key(mq_id))
        if not data:
            return dict()
        json_data = json.loads(data[5:])
        return json_data


def agent_chat_with_redis(data: ChatRequestData):
    chat_id = data.chat_id
    request_data = data.to_dict()
    request_data["created_at"] = time.time()
    request_data["total_tokens"] = 0
    request_data["total_context"] = ""

    # Cursor, ensure all data entering redis has an offset
    cursor = CursorObj()

    @ignore_exceptions
    def record_send_data(json_data):
        nonlocal request_data
        if json_data.get("dify_chunk", {}).get("event", "") == "sf_tokens":
            request_data["agent_name"] = json_data.get("agent_name", "")
            request_data["total_tokens"] += json_data.get("dify_chunk", {}).get("total_tokens", 0)
            request_data["total_context"] += json_data.get("dify_chunk", {}).get("total_answer", "") + "\n"

    @ignore_exceptions
    def record_send_msg(msg):
        nonlocal request_data
        if msg == AgentConstant.AGENT_CHAT_DONE_MSG:
            request_data["finish_at"] = time.time()
            ide_es_service.insert_data(request_data)

    def send_json_func(json_data):
        record_send_data(json_data)
        DifyMessageQueueHelper.push_json(chat_id, json_data, cursor)

    def send_msg_func(msg):
        record_send_msg(msg)
        DifyMessageQueueHelper.push_msg(chat_id, msg, cursor)

    agent_chat(data, send_json_func, send_msg_func)

def agent_chat(req: ChatRequestData, send_json_func, send_msg_func):
    """
    Generate dialogue data with agent and send it to the client requesting the dialogue
    """
    iostream = AgentChatIOStream(send_json_func=send_json_func, send_msg_func=send_msg_func)
    try:
        if req.prompt:
            with IOStream.set_default(iostream):
                chatbot = AgentChatBot(req.conversation_id, req.chat_id)
                chatbot.chat_stream(req, username=req.username)
    except Exception:
        # Print detailed information
        traceback.print_exc()
    finally:
        iostream.finish()
