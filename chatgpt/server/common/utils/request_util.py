#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 20:39
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 20:39
"""

import logging
import time
from urllib import parse

from requests_toolbelt import MultipartEncoder
import requests
import json
from common.helpers.custom_json_encoder import CustomJSONEncoder
from copy import deepcopy
from common.constant import AppConstant
# from lib.admin_notice import AdminNotice
# from common.constant import ErrorMsgs
from common.exception.exceptions import RequestError

logger = logging.getLogger(__name__)


class RequestUtil:
    headers = {'User-Agent': 'CICD Service', 'content-type': 'application/json'}
    conf = AppConstant
    default_retry = False

    @classmethod
    def get(cls, url, retry=None, *args, **kwargs):
        return cls.__request(url, method='GET', retry=retry, *args, **kwargs)

    @classmethod
    def post(cls, url, data=None, json=None, retry=None, *args, **kwargs):
        return cls.__request(url, method='POST', data=data, json=json, retry=retry, *args, **kwargs)

    @classmethod
    def form_post(cls, url, data=None, json=None, retry=None, *args, **kwargs):
        m = MultipartEncoder(fields=json)
        return requests.post(url, data=m, headers={'Content-Type': m.content_type})

    @classmethod
    def put(cls, url, data=None, json=None, retry=None, *args, **kwargs):
        return cls.__request(url, method='PUT', data=data, json=json, retry=retry, *args, **kwargs)

    @classmethod
    def delete(cls, url, retry=None, *args, **kwargs):
        return cls.__request(url, method='DELETE', retry=retry, *args, **kwargs)

    @classmethod
    def head(cls, url, retry=None, *args, **kwargs):
        return cls.__request(url, method='HEAD', retry=retry, *args, **kwargs)

    @classmethod
    def __request(cls, url, method='GET', retry=None, *args, **kwargs):
        retry = retry if retry is not None else cls.default_retry
        headers = deepcopy(cls.headers)
        if 'headers' in kwargs:
            if kwargs.get('headers') is not None:
                headers.update(kwargs['headers'])
            del kwargs['headers']
        try:
            convert_to_json = True
            if "convert_to_json" in kwargs and kwargs.pop("convert_to_json", True) is False:
                # 传参 convert_to_json 为 False 时不转成 json, 不指定content-type
                convert_to_json = False
                keys = []
                for key in headers:
                    if key.lower() == 'content-type':
                        keys.append(key)
                for key in keys:
                    del headers[key]

            if "data" in kwargs and convert_to_json:
                if kwargs.get("data") is not None:
                    data = json.dumps(kwargs.get("data"), cls=CustomJSONEncoder).encode('utf8')
                    kwargs['data'] = data
            return cls._request_with_retry(method, url, headers, retry, **kwargs)
        except ModuleNotFoundError as err:
            logger.error(f"请求404：{err}，直接抛出")
            raise ModuleNotFoundError(err)
        except Exception as e:
            logger.error(f"请求异常：{str(e)}, url:{url}", exc_info=True)
            if "401" in str(e):
                logger.error(f"401 error ++++++,kwargs: {str(kwargs)}, headers: {headers}")
            raise RequestError(f"服务或网络异常{e}")

    @classmethod
    def _make_response(cls, resp, raw=False):
        resp.encoding = resp.encoding if resp.encoding else "UTF-8"
        # 为了获取到td的错误信息，改为400
        if 200 <= resp.status_code < 300:
            if resp.status_code == 204:
                return None
            if raw:
                return resp
            return json.loads(resp.text)
        elif resp.status_code == 400:
            if raw:
                return resp
            return json.loads(resp.text)
        elif resp.status_code == 404:
            logger.info(f"远程请求结果：{resp.text}")
            raise ModuleNotFoundError(f"未找到：{resp.text}")
        else:
            logger.info(f"远程请求结果：{resp.text}")
            raise RuntimeError(f"远程获取出现异常：{resp.text}")

    @classmethod
    def _request_with_retry(cls, method, url, headers, retry, **kwargs):
        # 默认会重试5次，但这个没设置超时时间
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        # 是否返回响应对象
        raw = kwargs.pop("raw", False)
        #  如果指定了timeout参数，则不用配置中的重试时间
        timeout = kwargs.pop("timeout", None)
        if not retry:
            return cls._make_response(requests.request(method, url, headers=headers, **kwargs), raw=raw)

        retry_count = 0
        while retry_count < len(cls.conf.REQUESTS_TIMEOUT_TIME):
            try:
                result = cls._make_response(requests.request(
                    method, url, headers=headers,
                    timeout=timeout if timeout else cls.conf.REQUESTS_TIMEOUT_TIME[retry_count], **kwargs), raw=raw)
            except ModuleNotFoundError as err:
                logger.error(f"请求404：{err}，直接抛出")
                raise ModuleNotFoundError(err)
            except Exception as e:
                error_msg = f"请求异常：{str(e)}, url:{url}, retry_count:{retry_count}"
                logger.error(error_msg)
                # if ErrorMsgs.GITLAB_NOT_RESPONDE in str(e) and retry_count == 0:
                #     # gitlab 502无响应情况发送通知
                #     AdminNotice.notice(content=f"502: {str(error_msg)}", notice_type=AdminNotice.DIM)
                time.sleep(cls.conf.REQUESTS_TIMEOUT_TIME[retry_count])
                retry_count = retry_count + 1
                continue
            return result
        raise RequestError("服务或网络异常")

    @classmethod
    def urlencode(cls, url, params=None):
        if params is not None:
            params = parse.urlencode(params)
            url += '?{}'.format(params)
        return url


class RetryRequestUtil(RequestUtil):
    # 默认重试为True
    default_retry = True
