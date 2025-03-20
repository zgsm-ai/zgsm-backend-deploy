import socketio
import json
import re
from aiohttp import web

from controllers.socket.events import register_socketio
from db import db
from logger import get_socket_server_logger

server_logger = get_socket_server_logger()

class CustomJsonModule:
    def dumps(self, *args, **kwargs):
        try:
            return json.dumps(*args, **kwargs)
        except Exception as err:
            server_logger.error(f"json dumps error: {err}\norigin data: {args[0]}")
            raise err

    def loads(self, *args, **kwargs):
        try:
            return json.loads(*args, **kwargs)
        except Exception as err:
            content = args[0].strip()
            if content and content not in ["probe"]:
                # Determine whether the regular expression pattern matches "\d/(.*?)," which is normal, and only log the rest
                if not re.match(r"^\d+/.*?,", content):
                    server_logger.error(f"json loads error: {err}\norigin data: {content}")
            raise err


# Create a Socket.IO server instance
sio = socketio.AsyncServer(
    async_mode='aiohttp',
    cors_allowed_origins="*",
    ping_interval=60,
    ping_timeout=60,
    logger=False,
    engineio_logger=False,
    json=CustomJsonModule()
)
app = web.Application()
sio.attach(app)

db.init_database()
register_socketio(sio)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8765)
