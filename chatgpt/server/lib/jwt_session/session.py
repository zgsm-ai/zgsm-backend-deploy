import logging
import jwt
import datetime

from .local import Local

# 创建一个全局对象,用来存储session,或者其他的全局变量
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
        :param headers: 请求头
        :param cookies: cookies
        :param name: cookies的key名称
        :param secret: jwt密钥
        :param expire: 过期时间, 天
        :param kwargs: 其他参数
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
        # 先不做校验，容易误杀产品线的脚本
        self.access_ip = headers.get('X-Real-IP') if headers.get('X-Real-IP') else ''

    def parse(self, verify_expire=True, exp_key='exp'):
        """
        :param verify_expire: 是否验证过期
        :param exp_key: 验证过期的key
        :return: 解析的jwt_token结果
        """
        value = self._parse_key()
        if value:
            res = self.decode(value)
            if res and verify_expire:
                """验证过期时间"""
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
        验证结果是否过期
        :param res: 解析后的数据
        :param exp_key: 判断过期时间的key
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
        """解析jwt_token的key"""
        # 适配tp平台token为ep_jwt_token_current，多了“_current”
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
        # 加密
        return jwt.encode(payload, self.secret,
                          algorithm=self.algorithm).decode('ascii') if payload else None

    def decode(self, token):
        """解码"""
        try:
            return jwt.decode(
                token, self.secret, verify_expiration=False, algorithms=self.algorithm) if token else None
        except Exception as err:
            self.logger.warning(f"解析token：{token}出现异常:{str(err)}")
            return None

    @classmethod
    def create_token(cls, payload, secret, algorithm):
        # 临时生成token
        return jwt.encode(payload, secret, algorithm).decode('ascii') if payload else None
