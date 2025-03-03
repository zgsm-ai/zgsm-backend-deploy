import logging
import datetime

from lib.jwt_session.session import JwtTokenHandler
from common.helpers.application_context import ApplicationContext

from config import conf

logger = logging.getLogger(__name__)

NAME = conf.get("jwt", {}).get("NAME")
ALG = conf.get("jwt", {}).get("ALGORITHM")
EXP = conf.get("jwt", {}).get("EXPIRE")
SECRET = conf.get("jwt", {}).get("SECRET")
DOMAIN = conf.get("jwt", {}).get("DOMAIN")


class JwtTokenService:
    headers = dict(
        alg=ALG
    )

    def __init__(self, request):
        self.request = request

    def gen_token(self):
        headers = self.request.headers
        cookies = self.request.cookies
        jwt_handler = JwtTokenHandler(
            headers, cookies, NAME, SECRET, EXP, domain=DOMAIN, algorithm=ALG)
        payload = self._gen_payload(self.request)
        session = ApplicationContext.get_session()
        session.update(payload)
        return jwt_handler.encode(session.to_dict())

    def _gen_payload(self, request):
        current_user = ApplicationContext.get_current()
        return self._payload(
            username=current_user.username,
            display_name=current_user.display_name,
            is_admin=current_user.is_admin,
            email=current_user.email,
            access_ip=self.get_current_access_ip(request)
        ) if current_user else {}

    def _payload(self, username=None, display_name=None, is_admin=False,
                 email=None, access_ip=None, iat=None, exp=None):
        return dict(
            username=username,
            display_name=display_name,
            is_admin=is_admin,
            email=email,
            access_ip=access_ip,
            iat=iat if iat else datetime.datetime.now(),
            exp=exp if exp else self.get_expire(EXP)
        )

    @staticmethod
    def get_expire(days):
        return datetime.datetime.now() + datetime.timedelta(days=int(days))

    @staticmethod
    def get_current_access_ip(request):
        return request.headers.get('X-Real-IP') if request.headers.get(
            'X-Real-IP') else request.remote_addr

    @classmethod
    def create_token(cls, payload):
        """
        临时生成使用
        :param payload:  用户信息
        :return:
        """
        return JwtTokenHandler.create_token(payload, SECRET, ALG)

    @classmethod
    def get_jwt_token_header(cls, user):
        """
        获取header，选择使用
        :param user:
        :return:
        """
        user_info = {'username': user.username, 'display_name': user.display_name}
        _token = JwtTokenService.create_token(user_info)
        token = "ep_jwt_token=" + _token
        return {"cookie": token}, token
