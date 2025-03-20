#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Su Deli 16646
    :Time: 2023/3/14 20:39
    :Modifier: Su Deli 16646
    :UpdateTime: 2023/3/14 20:39
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
                # The json will not be converted to json when the parameter convert_to_json is False, and the content-type is not specified
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
            logger.error(f"Request 404：{err}，throw directly")
            raise ModuleNotFoundError(err)
        except Exception as e:
            logger.error(f"Request exception：{str(e)}, url:{url}", exc_info=True)
            if "401" in str(e):
                logger.error(f"401 error ++++++,kwargs: {str(kwargs)}, headers: {headers}")
            raise RequestError(f"Service or network exception{e}")

    @classmethod
    def _make_response(cls, resp, raw=False):
        resp.encoding = resp.encoding if resp.encoding else "UTF-8"
        # In order to get the error message of td, change it to 400
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
            logger.info(f"Remote request result：{resp.text}")
            raise ModuleNotFoundError(f"Not Found：{resp.text}")
        else:
            logger.info(f"Remote request result：{resp.text}")
            raise RuntimeError(f"Remote access exception：{resp.text}")

    @classmethod
    def _request_with_retry(cls, method, url, headers, retry, **kwargs):
        # The default will retry 5 times, but this does not set the timeout time
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        # Whether to return the response object
        raw = kwargs.pop("raw", False)
        # If the timeout parameter is specified, the retry time in the configuration is not used
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
                logger.error(f"Request 404：{err}，throw directly")
                raise ModuleNotFoundError(err)
            except Exception as e:
                error_msg = f"Request exception：{str(e)}, url:{url}, retry_count:{retry_count}"
                logger.error(error_msg)
                # if ErrorMsgs.GITLAB_NOT_RESPONDE in str(e) and retry_count == 0:
                #     # Send notification when gitlab 502 is unresponsive
                #     AdminNotice.notice(content=f"502: {str(error_msg)}", notice_type=AdminNotice.DIM)
                time.sleep(cls.conf.REQUESTS_TIMEOUT_TIME[retry_count])
                retry_count = retry_count + 1
                continue
            return result
        raise RequestError("Service or network exception")

    @classmethod
    def urlencode(cls, url, params=None):
        if params is not None:
            params = parse.urlencode(params)
            url += '?{}'.format(params)
        return url


class RetryRequestUtil(RequestUtil):
    # The default retry is True
    default_retry = True
