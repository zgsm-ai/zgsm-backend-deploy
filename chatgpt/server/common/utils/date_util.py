#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Su Deli 16646
    :Time: 2023/3/17 10:02
    :Modifier: Su Deli 16646
    :UpdateTime: 2023/3/17 10:02
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
        """Parse local time, any time zone time, timestamp (seconds)
        Returns local time native datetime (tzinfo is None)
        Throws an exception if parsing fails
        """
        if dt_str:
            try:
                dt_str = int(dt_str)
            except (ValueError, TypeError) as err:
                cls.logger.info(f"Parsing time error{str(err)}")
            if isinstance(dt_str, str):
                dt = parser.parse(dt_str)
            elif isinstance(dt_str, datetime.datetime):
                dt = dt_str
            else:
                dt = datetime.datetime.fromtimestamp(dt_str)
            # If there is time zone information, correctly convert it to local time zone time, and then erase the time zone information
            if dt.tzinfo:
                dt = dt.astimezone(cls.LOCAL_TZ)
                dt = dt.replace(tzinfo=None)
            return dt
        else:
            raise RuntimeError(f"Unparsable datetime format: {dt_str}")

    @classmethod
    def str_to_date(cls, string_value, format='%Y-%m-%d'):
        try:
            date_value = None
            if string_value:
                date_value = datetime.datetime.strptime(string_value, format)
            return date_value
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

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
            cls.logger.debug(f"Parameter conversion datetime exception: {str(err)}, trying to convert to date")

    @classmethod
    def get_now_yyyymmddhhmmss(cls):
        """
        Get the string of year, month, day, hour, minute and second

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
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{date_value} format error, please check the parameter format")

    @classmethod
    def datetime_to_str(cls, datetime_value, format=EAST_EIGHT_AREA):
        try:
            return datetime_value.strftime(format) if datetime_value else None
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Time:{datetime_value} format error, please check the parameter format")

    @classmethod
    def str_to_format_date(cls, string_value, source_format, target_format):
        try:
            if string_value:
                source_date = datetime.datetime.strptime(string_value, source_format)
                if source_date:
                    return cls.str_to_date(source_date.strftime(target_format), target_format)
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

    @classmethod
    def str_to_format_str_date(cls, string_value, source_format, target_format):
        try:
            if string_value:
                source_date = datetime.datetime.strptime(string_value, source_format)
                if source_date:
                    return source_date.strftime(target_format)
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

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
    #         cls.logger.debug(f"Parameter conversion exception: {str(err)}")
    #         raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

    @classmethod
    def str_to_format_gmt_datetime(cls, string_value):
        try:
            date_value = None
            if string_value:
                date_value = datetime.datetime.strptime(string_value, cls.EAST_EIGHT_AREA)
            return date_value
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

    @classmethod
    def str_to_gmt_datetime_str(cls, string_value):
        try:
            return cls.datetime_to_str(cls.str_to_datetime(string_value), cls.EAST_EIGHT_AREA)
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Date:{string_value} format error, please check the parameter format")

    @classmethod
    def is_equal(cls, datetime1, datetime2):
        """Compare whether two times are equal"""
        try:
            if not any([datetime1, datetime2]):  # If any parameter does not exist, return false directly
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
                cls.logger.info("The two dates are equal")
                return True
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError(f"Time:{datetime1} or {datetime2} format error, please check the parameter format")
        return False

    @classmethod
    def _str_to_datetime(cls, string_value):
        """
        Private method to convert a string to a datetime format
        Currently supports three formats: 1. %Y-%m-%d %H:%M:%S, 2. %Y-%m-%dT%H:%M:%S.000+0800, 3. %Y-%m-%dT%H:%M:%S%z
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
            cls.logger.error(f"Caught parameter conversion exception: {str(err)}")
        return None

    @classmethod
    def _str_to_date(cls, string_value):
        """Convert time string or date string to date"""
        try:
            datetime_value = cls._str_to_datetime(string_value)
            if datetime_value:
                return datetime_value.date()
            date_value = cls.str_to_date(string_value)
            if date_value:
                return date_value
        except Exception as err:
            cls.logger.error(f"Caught parameter conversion exception: {str(err)}")
        return None

    @classmethod
    def get_now_str(cls):
        try:
            return datetime.datetime.now().strftime(cls.EAST_EIGHT_AREA)
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError()

    @classmethod
    def get_now_datetime(cls):
        try:
            return datetime.datetime.now()
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError()

    @classmethod
    def calculate_days(cls, new_date):
        """
        Subtract the incoming time from today and return the number of days difference
        :param new_date: such as planned completion time
        :return: overdue days completed
        """
        return cls.a_sub_b(cls.get_now_datetime(), new_date)

    @classmethod
    def a_sub_b(cls, a, b):
        """
        Date a, minus date b return days
        :return: days
        """
        return (a - b).days if a and b else None

    @classmethod
    def get_now_date_str(cls):
        try:
            return datetime.datetime.now().strftime('%Y-%m-%d')
        except Exception as err:
            cls.logger.debug(f"Parameter conversion exception: {str(err)}")
            raise RuntimeError()

    @classmethod
    def generate_unique_md5(cls):
        # Get the current timestamp, accurate to nanoseconds
        current_time = str(time.time_ns())

        # Generate a random string
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # Combine the parameter string, current timestamp, and random string
        combined_str = current_time + random_str

        # Generate MD5 hash value
        md5_hash = hashlib.md5(combined_str.encode()).hexdigest()

        return md5_hash
