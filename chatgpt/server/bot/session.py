from OpenAIAuth import Authenticator, Error as AuthError
from .cache import get_redis


SESSION_CACHE_KEY = "session_token"


def do_login(config):
    auth = Authenticator(
        email_address=config.get("chatgpt_email"),
        password=config.get("chatgpt_password"),
        # proxy=config.get("proxy"),
    )
    auth.begin()
    auth.get_access_token()
    return auth.access_token


def refresh_session_token(config):
    session_token = do_login(config)
    if not session_token:
        raise AuthError
    save_session_token(config, session_token)
    return session_token


def get_session_token(config):
    redis = get_redis(config)
    session_token = redis.get(SESSION_CACHE_KEY)
    if not session_token:
        session_token = do_login(config)
        if not session_token:
            raise AuthError
        save_session_token(config, session_token)
    return session_token


def save_session_token(config, session_token):
    redis = get_redis(config)
    return redis.set(SESSION_CACHE_KEY, session_token)
