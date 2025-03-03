import asyncio
import socketio
import time
import jwt
import pytz
from datetime import datetime

from common.helpers.application_context import ApplicationContext
from services.agents.agent_chat_async import DifyMessageQueueHelper as dify_queue_helper
from common.constant import AgentConstant, LoggerNameContant
from common.exception.exceptions import NoLoginError
from config import conf
from third_platform.es.chat_messages.chat_es_service import chat_es
from logger import get_socket_server_logger

server_logger = get_socket_server_logger()

socket_pool = {}

def get_username_by_token(token: str): 
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded.get("preferred_username")

def get_current_user(auth):
    from services.system.users_service import UsersService
    # vscode-zgsm-v1.1.9之前版本只有'api-key'，没有username和display_name
    # vscode-zgsm-v1.1.10版本连'api-key'都没有
    user = None
    token = auth.get("token") if auth.get("token") else auth.get("api-key")
    if token:
        user = UsersService.get_user_by_api_key(token)
        if user:
            return user
    # 第一次使用，数据库还找不到记录
    username = auth.get("username")
    if not username:
        if token:
            #  已经通过用户系统的认证，获得了token
            username = get_username_by_token(token)
        else:
            #  没token，也没username，创建一个test用户顶着用，当是匿名登录
            user = UsersService.create_test_user()
            ApplicationContext.update_session_user(user)
            return user
    display_name = auth.get("display_name", "")
    host_ip = auth.get("host_ip", "")
    user = UsersService.create_zgsm_user(username, display_name, host_ip, token)
    if not user:
        return None
    ApplicationContext.update_session_user(user)
    return user


def get_current_user_in_socket(sid, auth=None):
    global socket_pool
    if auth:
        current_user = get_current_user(auth)
        if current_user:
            if sid:
                socket_pool[sid] = {"current_user": current_user, "auth": auth}
        return current_user
    else:
        if sid:
            return socket_pool.get(sid, {}).get("current_user")
        else:
            return None


def logout_user_in_socket(sid):
    global socket_pool
    if sid in socket_pool:
        del socket_pool[sid]


class ChatNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ, auth):
        current_user = get_current_user_in_socket(sid, auth)
        if not current_user:
            # 拒绝连接
            server_logger.error(f"Client connect failed, sid: {sid}, auth: {auth or '{}'}")
            return False
        server_logger.info(f"Client connected({sid}): {current_user.__dict__}")
        chat_es.insert_connect(sid, current_user)
        safe_environ = {k: v for k, v in environ.items() if isinstance(v, (str, int, float))}
        server_logger.debug(f"env: {safe_environ or '{}'}")
        server_logger.debug(f"auth: {auth or '{}'}")

    def on_disconnect(self, sid):
        logout_user_in_socket(sid)
        server_logger.info(f'Client disconnected({sid})')

    async def on_ping(self, sid, message):
        await self.emit("message", "pong", room=sid)

    async def send_message_loop(self, chat_id, sid, offset=0):
        """
        发送消息的循环，一直从消息缓冲区中读取消息发送给客户端，直到消息发送完毕，或超时
        :param chat_id: 聊天id
        :param sid: 客户端id
        :param offset: 消息偏移量
        :remarks 一般来说,chat_id和sid相同，但是如果客户端断开重连，sid会变化，此时chat_id不变
        """
        if not offset:
            offset = 0
        chat_timeout = conf.get("chat_timeout")
        last_time = int(time.time())
        while True:
            """
            消息通过类似缓冲区的形式取而不是使用队列
            因为客户端避免不了出现重连的情况，一旦重连之前服务端的消息就没法再次发送
            所以通过 offset 来记录客户端之前收到哪里再次执行时从断点开始
            """
            data = dify_queue_helper.get_data_by_offset(chat_id, offset)
            if not data:
                # FIXME: 如果传入的 chat_id 实际并不存在，这里会一直循环。考虑加个超时判断机制
                cur_time = int(time.time())
                if cur_time - last_time > chat_timeout:
                    server_logger.error(f"Chat timeout, sid: {sid}, chat_id: {chat_id}")
                    await self.emit('error', "Chat timeout", room=sid)
                    break
                await asyncio.sleep(0)
            else:
                last_time = int(time.time())
                if isinstance(data, dict):
                    await self.emit('json', data, room=sid)
                elif isinstance(data, str):
                    await self.emit('message', data, room=sid)
                    if data == AgentConstant.AGENT_CHAT_DONE_MSG:
                        break
                # 取到消息后才能更新 offset。offset 的顺序由 dify_queue_helper 内部进行管理和保障
                offset += 1
        server_logger.info(f"Send message(sid={sid},chat_id={chat_id}) finish: count={offset}")

    async def on_chat(self, sid, request_data: dict):
        server_logger.info(f'Received message({sid}) in chat: {request_data}')
        current_user = get_current_user_in_socket(sid)
        # 使用chat_id作为每次返回给前端的内容, 也就是存储在redis的内容
        chat_id = sid
        if not current_user:
            raise NoLoginError()

        from tasks.chat_task import execute_chat_async
        request_data["created_at"] = datetime.now(pytz.timezone('Asia/Shanghai'))
        request_data["ide"] = socket_pool.get(sid, {}).get("auth", {}).get('ide', '')
        request_data["ide_version"] = socket_pool.get(sid, {}).get("auth", {}).get('ide-version', '')
        request_data["ide_real_version"] = socket_pool.get(sid, {}).get("auth", {}).get('ide-real-version', '')
        request_data["username"] = current_user.username
        request_data["display_name"] = current_user.display_name
        request_data["chat_id"] = chat_id
        execute_chat_async.delay(
            sid=sid,
            request_data=request_data
        )
        chat_es.insert_chat(sid, request_data)

        # 发送 chat_id 给前端，前端若出现断联则可以通过 chat_id 重新连接
        await self.emit("updateChatId", chat_id, room=sid)
        await self.send_message_loop(chat_id, sid)

    async def on_rechat(self, sid, request_data):
        chat_id = request_data.get("chat_id")
        offset = request_data.get("offset", 0)
        server_logger.info(f'Received rechat request: {request_data}')
        if chat_id:
            await self.send_message_loop(chat_id, sid, offset)


def register_socketio(socketio):
    # 注册自定义命名空间
    socketio.register_namespace(ChatNamespace('/chat'))
