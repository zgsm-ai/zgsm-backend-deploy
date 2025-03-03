#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from contextlib import contextmanager
from functools import wraps
import redis_lock

from common.exception.exceptions import LockFail
from .redis import BaseCache

logger = logging.getLogger(__name__)
EXPIRE = 60


def get_locker(name: str, **kwargs):
    return redis_lock.Lock(BaseCache().connection, name, **kwargs)


def parameter_lock(key=None, index=None, prefix_key=None, blocking=True, lock_exist_return=None, fail_run=False,
                   timeout=EXPIRE):
    """
    带参数的锁，支持用参数进行加锁，位置参数和命名参数
    :param key: 命名参数时，参数名
    :param index: 位置参数时，参数位置值，下标从0开始
    :param prefix_key: 加锁的key前缀, 没有传就用被锁的函数名
    :param blocking: 遇到相同key，False（跳过不执行）， True(进入排队，继续执行)
    :param lock_exist_return: 遇到相同key，跳过不执行的返回值
    :param fail_run: 锁定失败是否执行
    :param timeout: 锁定超时时间
    :return:
    """

    def lock_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if key in kwargs:
                suffix_key = kwargs.get(key)
            else:
                suffix_key = args[index]

            redis_key = f'lock:{prefix_key}:{suffix_key}' if prefix_key else f'lock:{func.__qualname__}:{suffix_key}'

            logger.info(f'尝试锁定函数{func.__qualname__}:{redis_key},cache.connection:{BaseCache().connection}')
            locker = redis_lock.Lock(BaseCache().connection, redis_key, expire=timeout)

            try:
                if blocking:
                    result = locker.acquire(timeout=timeout)
                    # 表示等待到超时也未拿到锁，返回是false
                    if not result:
                        raise redis_lock.NotAcquired("获取锁超时未拿到锁")
                else:
                    if not locker.acquire(blocking=blocking):
                        logger.info(f'锁定函数{func.__qualname__}:{redis_key}失败，已存在')
                        return lock_exist_return

                logger.info(f'锁定函数{func.__qualname__}:{redis_key}成功')
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"执行函数{func.__qualname__}:{redis_key}失败, error: {e}", exc_info=True)
                    raise e
                finally:
                    try:
                        locker.release()
                        logger.info(f'释放函数{func.__qualname__}:{redis_key}成功')
                    except redis_lock.NotAcquired as e:
                        logger.error(
                            f'释放函数{func.__qualname__}:{redis_key}失败，error: {e},{locker._client}', exc_info=True)
            except redis_lock.NotAcquired as e:
                if fail_run:
                    logger.error(f'锁定函数{func.__qualname__}:{redis_key}失败，直接执行, error: {e}', exc_info=True)
                    try:
                        ret = func(*args, **kwargs)
                    except Exception as e:
                        logger.error(f"非锁定情况执行函数{func.__qualname__}:{redis_key}失败, error: {e}",
                                     exc_info=True)
                        raise e
                else:
                    logger.info(f'锁定函数{func.__qualname__}:{redis_key}失败，不执行, {e}', exc_info=True)
                    return lock_exist_return

            except Exception as e:
                logger.error(f"锁定函数{func.__qualname__}:{redis_key}失败, error: {e}", exc_info=True)
                # 非“获得锁”失败，导致的异常，继续向上抛出
                raise e

            return ret

        return wrapper

    return lock_func


def data_lock(generate_data_id_method=None, job_name='unknown', blocking=True, wait_for=None, wait_blocking=True,
              fail_run=False):
    """
    带参数的数据互斥锁，数据粒度的锁，用于多个地方同时处理同一条数据，防止两边同时并发进行，保持两边先后顺序，保证数据的完整性
    :param generate_data_id_method 生成数据id的方法 该方法必须是一个可以调用的对象用于生成数据ID
    :param job_name: 任务名称（唯一） 默认为 默认 unknown
    :param wait_for: 是否需要等待对方的 方法/应用执行完成 默认 None
    :param wait_block: 是否以阻塞的方式等待对方的 方法/应用执行完成 默认 True
    :param blocking: 是否以阻塞等待的方式去获取自己的锁 默认 True
    :param fail_run: 锁定失败是否执行 默认 False
    :return:
    """

    def lock_func(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 没有传获取数据id的方法名称 or 没有定义该方法 or 该方法不能调用 都不处理直接抛异常
            if not generate_data_id_method or not hasattr(self, generate_data_id_method) \
                    or not callable(getattr(self, generate_data_id_method)):
                raise ValueError(f'{func.__qualname__}获取数据id 失败')

            data_id = getattr(self, generate_data_id_method)()
            redis_key = f'lock:data_lock:{job_name}:{data_id}'
            log_msg = f'数据锁 锁定数据{job_name}函数{func.__qualname__} key:{redis_key}'
            self_locker = get_locker(name=redis_key, expire=EXPIRE)

            wait_for_key = f'lock:data_lock:{wait_for}:{data_id}'
            wait_log_msg = f'数据锁 {job_name}函数{func.__qualname__} key:{redis_key} 等待 {wait_for} key:{wait_for_key}任务'
            wait_for_locker = get_locker(name=wait_for_key, expire=EXPIRE)

            try:
                # 自己job_name 不能和 wait_for 的任务名一样
                if job_name == wait_for:
                    raise ValueError('job_name 不能和 wait_for 一样')

                # 如果需要等待其它任务先执行，则先去获取等待目标的锁是否存在
                if wait_for:
                    # 获取对方的锁
                    # 对方的锁已存在 拿不到锁 则根据wait_blocking 来指定是否阻塞等待
                    # 对方的锁不存在 拿到了锁 则继续往下执行
                    try:
                        logging.info(wait_log_msg + ' 开始获取对方锁')
                        if not wait_for_locker.acquire(blocking=wait_blocking):
                            raise LockFail(wait_for)
                    except redis_lock.NotAcquired:
                        raise LockFail(wait_for)
                    logging.info(wait_log_msg + ' 已经获取到对方锁')

                # 获取锁
                try:
                    if not self_locker.acquire(blocking=blocking):
                        raise LockFail(job_name)
                except redis_lock.NotAcquired:
                    raise LockFail(job_name)

                # 加锁成功开始执行
                try:
                    ret = func(self, *args, **kwargs)
                except Exception as e:
                    logging.error(log_msg + f'执行函数错误：{e}')
                    raise e
                finally:
                    try:
                        self_locker.release()
                        logging.info(log_msg + ' 释放锁 成功')
                    except redis_lock.NotAcquired:
                        logging.info(log_msg + ' 释放锁 失败')

                    try:
                        wait_for_locker.release()
                        logging.info(wait_log_msg + ' 释放对方锁 成功')
                    except redis_lock.NotAcquired:
                        logging.info(wait_log_msg + ' 释放对方锁 失败')

            except Exception as e:
                # 如果是LockFail异常 并且 fail_run 是True 任然继续执行
                if isinstance(e, LockFail):
                    if e.args[0] == wait_for:
                        logging.info(wait_log_msg + ' 获取对方的锁失败')

                    # 获取是获取自己锁失败的时候 ，则需要释放对方的锁
                    if e.args[0] == job_name:
                        try:
                            wait_for_locker.release()
                            logging.info(wait_log_msg + ' 释放锁对方锁 成功')
                        except redis_lock.NotAcquired:
                            logging.info(wait_log_msg + ' 释放锁对方锁 失败')

                    logging.error(log_msg + f'加锁失败, error:{e}', exc_info=True)
                    if fail_run:
                        logging.info(log_msg + f'锁定失败，直接执行, error:{e}', exc_info=True)
                        try:
                            ret = func(self, *args, **kwargs)
                        except Exception as e:
                            logging.error(log_msg + f"锁定失败后执行异常, error: {e}", exc_info=True)
                            raise e
                        return ret
                    else:
                        logging.info(log_msg + f'锁定失败后不执行, error:{e}', exc_info=True)
                        raise e

                else:
                    # 其它错误则释放锁后直接抛出异常
                    try:
                        self_locker.release()
                    except redis_lock.NotAcquired:
                        logging.info(log_msg + ' 释放锁 成功')
                    # 释放对方的锁
                    try:
                        wait_for_locker.release()
                        logging.info(wait_log_msg + ' 释放锁对方锁 成功')
                    except redis_lock.NotAcquired:
                        logging.info(wait_log_msg + ' 释放锁对方锁 失败')

                    raise e

            return ret

        return wrapper

    return lock_func


def release_all_lock():
    # 重启服务时候清除掉锁，防止死锁
    keys = BaseCache().connection.keys('lock*')
    for k in keys:
        BaseCache().connection.delete(k)


def lock_timed_task(func):
    """
    60秒内同一个函数，同样的参数，只允许执行一次
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = f'lock:{func.__qualname__}:{args}:{kwargs}'
        if BaseCache().set(key, 1, nx=True, ex=EXPIRE):
            return func(self, *args, **kwargs)
        else:
            logging.info(f'{key}在{EXPIRE}秒内已经存在')

    return wrapper


@contextmanager
def named_lock(name):
    """
    命名锁
    :param name:
    :type name:
    :return:
    :rtype:
    """
    locker = redis_lock.Lock(BaseCache().connection, str(name))
    try:
        yield locker.acquire()
    finally:
        try:
            locker.release()
        except redis_lock.NotAcquired:
            logging.error(f'{name}锁已经被释放')
