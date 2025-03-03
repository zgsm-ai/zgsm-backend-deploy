#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/17 10:02
    :修改者: 苏德利 16646
    :更新时间: 2023/3/17 10:02
"""

import datetime
import logging
# import math
from dateutil import parser, tz
import hashlib
import time
import random
import string


class DateUtil:
    logger = logging.getLogger(__name__)

    EAST_EIGHT_AREA = "%Y-%m-%dT%H:%M:%S.000+0800"
    Y_M_D_T_H_M_SZ = "%Y-%m-%dT%H:%M:%S.000Z"
    Y_M_D = "%Y-%m-%d"
    LOCAL_TZ = tz.tzlocal()

    HALFDAY_BOUNDARY = 12

    @classmethod
    def parse_to_local(cls, dt_str):
        """解析 本地时间、任何时区时间、时间戳（秒）
        返回本地时间 native datetime (tzinfo 为 None)
        解析出现问题抛异常
        """
        if dt_str:
            try:
                dt_str = int(dt_str)
            except (ValueError, TypeError) as err:
                cls.logger.info(f"解析时间出错{str(err)}")
            if isinstance(dt_str, str):
                dt = parser.parse(dt_str)
            elif isinstance(dt_str, datetime.datetime):
                dt = dt_str
            else:
                dt = datetime.datetime.fromtimestamp(dt_str)
            # 如果有时区信息，将其正确转换为本地时区时间，然后将时区信息抹除
            if dt.tzinfo:
                dt = dt.astimezone(cls.LOCAL_TZ)
                dt = dt.replace(tzinfo=None)
            return dt
        else:
            raise RuntimeError(f"无法解析的 datetime 格式：{dt_str}")

    @classmethod
    def str_to_date(cls, string_value, format='%Y-%m-%d'):
        try:
            date_value = None
            if string_value:
                date_value = datetime.datetime.strptime(string_value, format)
            return date_value
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    @classmethod
    def str_to_datetime(cls, string_value, format='%Y-%m-%d %H:%M:%S'):
        try:
            if string_value:
                try:
                    return datetime.datetime.strptime(string_value, format)
                except Exception:
                    try:
                        return datetime.datetime.strptime(string_value, cls.EAST_EIGHT_AREA)
                    except Exception:
                        try:
                            return datetime.datetime.strptime(string_value, cls.Y_M_D_T_H_M_SZ)
                        except Exception:
                            return cls.str_to_date(string_value)
        except Exception as err:
            cls.logger.debug(f"参数转换datetime异常：{str(err)}, 尝试转换成date")

    @classmethod
    def get_now_yyyymmddhhmmss(cls):
        """
        获取年月日时分秒的字符串

        :return: 20210915085527251
        """
        now = cls.get_now_datetime()
        return f"{now.year}{'%0.2d' % now.month}{'%0.2d' % now.day}{'%0.2d' % now.hour}{'%0.2d' % now.minute}" \
               f"{'%0.2d' % now.second}"

    @classmethod
    def date_to_str(cls, date_value, format='%Y-%m-%d'):
        try:
            if date_value:
                return date_value.strftime(format)
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{date_value}格式错误，请检查参数格式")

    @classmethod
    def datetime_to_str(cls, datetime_value, format=EAST_EIGHT_AREA):
        try:
            return datetime_value.strftime(format) if datetime_value else None
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"时间:{datetime_value}格式错误，请检查参数格式")

    @classmethod
    def str_to_format_date(cls, string_value, source_format, target_format):
        try:
            if string_value:
                source_date = datetime.datetime.strptime(string_value, source_format)
                if source_date:
                    return cls.str_to_date(source_date.strftime(target_format), target_format)
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    @classmethod
    def str_to_format_str_date(cls, string_value, source_format, target_format):
        try:
            if string_value:
                source_date = datetime.datetime.strptime(string_value, source_format)
                if source_date:
                    return source_date.strftime(target_format)
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    # @classmethod
    # def str_to_format_str(cls, string_value):
    #     try:
    #         if string_value:
    #             try:
    #                 return datetime.datetime.strptime(string_value, cls.Y_M_D)
    #             except Exception:
    #                 pass
    #             try:
    #                 return datetime.datetime.strptime(string_value, cls.EAST_EIGHT_AREA)
    #             except Exception:
    #                 pass
    #     except Exception as err:
    #         cls.logger.debug(f"参数转换异常：{str(err)}")
    #         raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    @classmethod
    def str_to_format_gmt_datetime(cls, string_value):
        try:
            date_value = None
            if string_value:
                date_value = datetime.datetime.strptime(string_value, cls.EAST_EIGHT_AREA)
            return date_value
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    @classmethod
    def str_to_gmt_datetime_str(cls, string_value):
        try:
            return cls.datetime_to_str(cls.str_to_datetime(string_value), cls.EAST_EIGHT_AREA)
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"日期:{string_value}格式错误，请检查参数格式")

    @classmethod
    def is_equal(cls, datetime1, datetime2):
        """比较两个时间是否相等"""
        try:
            if not any([datetime1, datetime2]):  # 某个参数不存在则直接返回false
                return False
            new_time1 = None
            new_time2 = None
            if isinstance(datetime1, datetime.datetime):
                new_time1 = int(round(time.mktime(datetime1.timetuple()) * 1000))
            elif isinstance(datetime1, str):
                _datetime1 = cls._str_to_datetime(datetime1)
                if _datetime1:
                    new_time1 = int(round(time.mktime(_datetime1.timetuple()) * 1000))
            if isinstance(datetime2, datetime.datetime):
                new_time2 = int(round(time.mktime(datetime2.timetuple()) * 1000))
            elif isinstance(datetime2, str):
                _datetime2 = cls._str_to_datetime(datetime2)
                if _datetime2:
                    new_time2 = int(round(time.mktime(_datetime2.timetuple()) * 1000))
            if new_time1 and new_time2 and new_time1 == new_time2:
                cls.logger.info("两个日期相等")
                return True
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError(f"时间:{datetime1}或{datetime2}格式错误，请检查参数格式")
        return False

    @classmethod
    def _str_to_datetime(cls, string_value):
        """
        私有方法，将字符串转换为日期时间格式
        暂时支持三种格式:1、%Y-%m-%d %H:%M:%S，2、%Y-%m-%dT%H:%M:%S.000+0800，3、%Y-%m-%dT%H:%M:%S%z
        :param string_value:
        :return:
        """
        try:
            datetime_value = cls.str_to_datetime(string_value)
            if datetime_value:
                return datetime_value
            datetime_value = cls.str_to_datetime(string_value, cls.EAST_EIGHT_AREA)
            if datetime_value:
                return datetime_value
            datetime_value = cls.str_to_datetime(string_value, '%Y-%m-%dT%H:%M:%S%z')
            if datetime_value:
                return datetime_value
        except Exception as err:
            cls.logger.error(f"捕获参数转换异常：{str(err)}")
        return None

    @classmethod
    def _str_to_date(cls, string_value):
        """将时间字符串或日期字符串转换为日期"""
        try:
            datetime_value = cls._str_to_datetime(string_value)
            if datetime_value:
                return datetime_value.date()
            date_value = cls.str_to_date(string_value)
            if date_value:
                return date_value
        except Exception as err:
            cls.logger.error(f"捕获参数转换异常：{str(err)}")
        return None

    @classmethod
    def get_now_str(cls):
        try:
            return datetime.datetime.now().strftime(cls.EAST_EIGHT_AREA)
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError()

    @classmethod
    def get_now_datetime(cls):
        try:
            return datetime.datetime.now()
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError()

    @classmethod
    def calculate_days(cls, new_date):
        """
        用今天 减去 传入时间，返回相差天数
        :param new_date: 如计划完成时间
        :return: 完成的超期天数
        """
        return cls.a_sub_b(cls.get_now_datetime(), new_date)

    @classmethod
    def a_sub_b(cls, a, b):
        """
        日期a, 减去日期b 返回天数
        :return: 天数
        """
        return (a - b).days if a and b else None

    @classmethod
    def get_now_date_str(cls):
        try:
            return datetime.datetime.now().strftime('%Y-%m-%d')
        except Exception as err:
            cls.logger.debug(f"参数转换异常：{str(err)}")
            raise RuntimeError()

    @classmethod
    def generate_unique_md5(cls):
        # 获取当前时间戳，精确到纳秒
        current_time = str(time.time_ns())

        # 生成一个随机字符串
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # 将参数字符串、当前时间戳和随机字符串结合起来
        combined_str = current_time + random_str

        # 生成 MD5 哈希值
        md5_hash = hashlib.md5(combined_str.encode()).hexdigest()

        return md5_hash
