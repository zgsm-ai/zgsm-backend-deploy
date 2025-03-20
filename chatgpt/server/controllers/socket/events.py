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
    # vscode-zgsm-v1.1.9 before versions only have 'api-key', without username and display_name
    # vscode-zgsm-v1.1.10 versions even don't have 'api-key'
    user = None
    token = auth.get("token") if auth.get("token") else auth.get("api-key")
    if token:
        user = UsersService.get_user_by_api_key(token)
        if user:
            return user
    # First use, the database cannot find the record
    username = auth.get("username")
    if not username:
        if token:
            # Authenticated by the user system and obtained a token
            username = get_username_by_token(token)
        else:
            # No token and no username, create a test user to use as an anonymous login
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
            # Reject connection
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
        A loop for sending messages, continuously reading messages from the message buffer and sending them to the client, until the messages are sent or a timeout occurs
        :param chat_id: chat id
        :param sid: client id
        :param offset: message offset
        :remarks Generally, chat_id and sid are the same, but if the client disconnects and reconnects, sid will change, but chat_id remains the same
        """
        if not offset:
            offset = 0
        chat_timeout = conf.get("chat_timeout")
        last_time = int(time.time())
        while True:
            """
            Messages are retrieved through a buffer-like form instead of using a queue
            Because clients inevitably experience reconnection, once reconnected, previous server messages cannot be resent
            Therefore, the offset is used to record where the client previously received and restart from the breakpoint when executing again
            """
            data = dify_queue_helper.get_data_by_offset(chat_id, offset)
            if not data:
                # FIXME: If the passed chat_id does not actually exist, it will loop continuously. Consider adding a timeout judgment mechanism
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
                # Offset can only be updated after the message is retrieved. The order of offset is managed and guaranteed internally by dify_queue_helper
                offset += 1
        server_logger.info(f"Send message(sid={sid},chat_id={chat_id}) finish: count={offset}")

    async def on_chat(self, sid, request_data: dict):
        server_logger.info(f'Received message({sid}) in chat: {request_data}')
        current_user = get_current_user_in_socket(sid)
        # Use chat_id as the content returned to the frontend each time, which is the content stored in redis
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

        # Send chat_id to the frontend, which can reconnect through chat_id if disconnected
        await self.emit("updateChatId", chat_id, room=sid)
        await self.send_message_loop(chat_id, sid)

    async def on_rechat(self, sid, request_data):
        chat_id = request_data.get("chat_id")
        offset = request_data.get("offset", 0)
        server_logger.info(f'Received rechat request: {request_data}')
        if chat_id:
            await self.send_message_loop(chat_id, sid, offset)


def register_socketio(socketio):
    # Register custom namespace
    socketio.register_namespace(ChatNamespace('/chat'))
