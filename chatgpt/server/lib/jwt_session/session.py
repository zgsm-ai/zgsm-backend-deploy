import logging
import jwt
import datetime

from .local import Local

# create a global object to store session or other global variables
session = Local()


class JwtSession(dict):
    pass


class NullSession(dict):
    pass


class JwtTokenHandler:
    default_alg = 'H256'
    logger = logging.getLogger(__name__)

    def __init__(self, headers, cookies, name, secret, expire, **kwargs):
        """
        :param headers: request header
        :param cookies: cookies
        :param name: key name of cookies
        :param secret: jwt secret key
        :param expire: expiration time, days
        :param kwargs: other parameters
        """
        self.headers = headers
        self.cookies = cookies
        self.name = name
        self.secret = secret
        self.expire = expire
        self.session = None
        self.domain = ""
        self.algorithm = self.default_alg
        if 'domain' in kwargs:
            self.domain = kwargs.get('domain')
        if 'algorithm' in kwargs:
            self.algorithm = kwargs.get('algorithm')
        # Do not verify for now, as it is easy to kill product line scripts by mistake
        self.access_ip = headers.get('X-Real-IP') if headers.get('X-Real-IP') else ''

    def parse(self, verify_expire=True, exp_key='exp'):
        """
        :param verify_expire: whether to verify expiration
        :param exp_key: key to verify expiration
        :return: parsed jwt_token result
        """
        value = self._parse_key()
        if value:
            res = self.decode(value)
            if res and verify_expire:
                """Verify expiration time"""
                is_expire = self._is_expire(res, exp_key)
                if not is_expire:
                    return JwtSession(res)
            if res is not None:
                return JwtSession(res)
        return NullSession({})

    def verify_access_ip(self):
        pass

    @staticmethod
    def _is_expire(res: dict, exp_key: str):
        """
        Verify whether the result has expired
        :param res: parsed data
        :param exp_key: key to determine expiration time
        :return:
        """
        if exp_key not in res:
            return True
        exp = res.get(exp_key)
        assert isinstance(exp, float) or isinstance(exp, int)
        now = datetime.datetime.now().timestamp()
        if (exp - now) < 0:
            return True
        return False

    def _parse_key(self):
        """Parse jwt_token's key"""
        # Adapt to tp platform, token is ep_jwt_token_current, with more "_current"
        cookie_value = self.cookies.get(self.name) if self.cookies and self.cookies.get(
            self.name) else self.cookies.get(f'{self.name}_current', '')
        if cookie_value and cookie_value != 'None' and cookie_value != 'undefined':
            return cookie_value
        header_value = self.headers.get(self.name) if self.headers and self.headers.get(
            self.name) else self.headers.get(f'{self.name}_current', '')
        if header_value and header_value != 'None' and header_value != 'undefined':
            return header_value
        return None

    def encode(self, payload):
        # encryption
        return jwt.encode(payload, self.secret,
                          algorithm=self.algorithm).decode('ascii') if payload else None

    def decode(self, token):
        """decode"""
        try:
            return jwt.decode(
                token, self.secret, verify_expiration=False, algorithms=self.algorithm) if token else None
        except Exception as err:
            self.logger.warning(f"Exception occurred while parsing token：{token}:{str(err)}")
            return None

    @classmethod
    def create_token(cls, payload, secret, algorithm):
        # temporary generate token
        return jwt.encode(payload, secret, algorithm).decode('ascii') if payload else None
