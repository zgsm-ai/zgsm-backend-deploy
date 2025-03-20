from common.constant import AgentConstant
from services.agents.agent_data_classes import ChatRequestData, make_cls_with_dict
from services.agents.agent_chat_async import agent_chat_with_redis
from tasks import celery_app, handle_db
from lib.log import SocketWrapper
from logger import get_task_chat_logger


@celery_app.task(queue=AgentConstant.TASK_CHAT_QUEUE,
                 soft_time_limit=AgentConstant.CELERY_TASK_TIMEOUT)
@handle_db
def execute_chat_async(sid: str, request_data: dict):
    # get_task_chat_logger log encapsulates sid and must be placed in the front
    logger = get_task_chat_logger()
    with SocketWrapper.with_sid(logger, sid):
        # Take out the uuid to get the context cache data from redis
        logger.info(f"execute_chat_async() start: request: {request_data}")
        req = make_cls_with_dict(ChatRequestData, request_data)
        agent_chat_with_redis(req)
        logger.info(f"execute_chat_async() finished")
