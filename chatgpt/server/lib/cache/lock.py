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
    Parameter lock, supports locking with parameters, positional and named arguments
    :param key: Parameter name when using named parameters
    :param index: Parameter position value when using positional parameters, index starts from 0
    :param prefix_key: Lock key prefix, if not provided, the locked function name is used
    :param blocking: When encountering the same key, False (skip execution), True (queue up, continue execution)
    :param lock_exist_return: Return value when skipping execution due to the same key
    :param fail_run: Whether to execute when locking fails
    :param timeout: Lock timeout
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

            logger.info(f'Attempting to lock function {func.__qualname__}:{redis_key}, cache.connection:{BaseCache().connection}')
            locker = redis_lock.Lock(BaseCache().connection, redis_key, expire=timeout)

            try:
                if blocking:
                    result = locker.acquire(timeout=timeout)
                    # False means timeout occurred without getting the lock
                    if not result:
                        raise redis_lock.NotAcquired("Failed to acquire lock within timeout period")
                else:
                    if not locker.acquire(blocking=blocking):
                        logger.info(f'Failed to lock function {func.__qualname__}:{redis_key}, already exists')
                        return lock_exist_return

                logger.info(f'Successfully locked function {func.__qualname__}:{redis_key}')
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Failed to execute function {func.__qualname__}:{redis_key}, error: {e}", exc_info=True)
                    raise e
                finally:
                    try:
                        locker.release()
                        logger.info(f'Successfully released function {func.__qualname__}:{redis_key}')
                    except redis_lock.NotAcquired as e:
                        logger.error(
                            f'Failed to release function {func.__qualname__}:{redis_key}, error: {e}, {locker._client}', exc_info=True)
            except redis_lock.NotAcquired as e:
                if fail_run:
                    logger.error(f'Failed to lock function {func.__qualname__}:{redis_key}, executing directly, error: {e}', exc_info=True)
                    try:
                        ret = func(*args, **kwargs)
                    except Exception as e:
                        logger.error(f"Failed to execute function {func.__qualname__}:{redis_key} without lock, error: {e}",
                                     exc_info=True)
                        raise e
                else:
                    logger.info(f'Failed to lock function {func.__qualname__}:{redis_key}, not executing, {e}', exc_info=True)
                    return lock_exist_return

            except Exception as e:
                logger.error(f"Failed to lock function {func.__qualname__}:{redis_key}, error: {e}", exc_info=True)
                # For exceptions not related to acquiring the lock, continue to raise
                raise e

            return ret

        return wrapper

    return lock_func


def data_lock(generate_data_id_method=None, job_name='unknown', blocking=True, wait_for=None, wait_blocking=True,
              fail_run=False):
    """
    Data mutex lock with parameters, a lock at the data granularity, used when multiple places process the same data simultaneously.
    Prevents concurrent execution, ensures sequential order, and maintains data integrity.
    :param generate_data_id_method: Method to generate data ID, must be a callable object that generates a data ID
    :param job_name: Task name (unique), default is 'unknown'
    :param wait_for: Whether to wait for the other method/application to complete, default None
    :param wait_blocking: Whether to wait for the other method/application to complete in a blocking manner, default True
    :param blocking: Whether to wait for your own lock in a blocking manner, default True
    :param fail_run: Whether to execute when locking fails, default False
    :return:
    """

    def lock_func(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # If no method name is provided to get the data id, or the method is not defined, or the method is not callable, throw an exception
            if not generate_data_id_method or not hasattr(self, generate_data_id_method) \
                    or not callable(getattr(self, generate_data_id_method)):
                raise ValueError(f'{func.__qualname__} failed to get data id')

            data_id = getattr(self, generate_data_id_method)()
            redis_key = f'lock:data_lock:{job_name}:{data_id}'
            log_msg = f'Data lock locking data {job_name} function {func.__qualname__} key:{redis_key}'
            self_locker = get_locker(name=redis_key, expire=EXPIRE)

            wait_for_key = f'lock:data_lock:{wait_for}:{data_id}'
            wait_log_msg = f'Data lock {job_name} function {func.__qualname__} key:{redis_key} waiting for {wait_for} key:{wait_for_key} task'
            wait_for_locker = get_locker(name=wait_for_key, expire=EXPIRE)

            try:
                # Your job_name cannot be the same as wait_for's task name
                if job_name == wait_for:
                    raise ValueError('job_name cannot be the same as wait_for')

                # If you need to wait for other tasks to execute first, check if the target's lock exists
                if wait_for:
                    # Get the other party's lock
                    # If the other's lock already exists and you can't get it, follow wait_blocking to determine whether to block and wait
                    # If the other's lock doesn't exist and you get it, continue execution
                    try:
                        logging.info(wait_log_msg + ' Starting to acquire the other party\'s lock')
                        if not wait_for_locker.acquire(blocking=wait_blocking):
                            raise LockFail(wait_for)
                    except redis_lock.NotAcquired:
                        raise LockFail(wait_for)
                    logging.info(wait_log_msg + ' Successfully acquired the other party\'s lock')

                # Get lock
                try:
                    if not self_locker.acquire(blocking=blocking):
                        raise LockFail(job_name)
                except redis_lock.NotAcquired:
                    raise LockFail(job_name)

                # Start execution after successful locking
                try:
                    ret = func(self, *args, **kwargs)
                except Exception as e:
                    logging.error(log_msg + f'Function execution error: {e}')
                    raise e
                finally:
                    try:
                        self_locker.release()
                        logging.info(log_msg + ' Lock released successfully')
                    except redis_lock.NotAcquired:
                        logging.info(log_msg + ' Failed to release lock')

                    try:
                        wait_for_locker.release()
                        logging.info(wait_log_msg + ' Released the other party\'s lock successfully')
                    except redis_lock.NotAcquired:
                        logging.info(wait_log_msg + ' Failed to release the other party\'s lock')

            except Exception as e:
                # If it's a LockFail exception and fail_run is True, continue execution
                if isinstance(e, LockFail):
                    if e.args[0] == wait_for:
                        logging.info(wait_log_msg + ' Failed to acquire the other party\'s lock')

                    # If it fails to acquire your own lock, release the other party's lock
                    if e.args[0] == job_name:
                        try:
                            wait_for_locker.release()
                            logging.info(wait_log_msg + ' Released the other party\'s lock successfully')
                        except redis_lock.NotAcquired:
                            logging.info(wait_log_msg + ' Failed to release the other party\'s lock')

                    logging.error(log_msg + f'Lock acquisition failed, error:{e}', exc_info=True)
                    if fail_run:
                        logging.info(log_msg + f'Lock failed, executing directly, error:{e}', exc_info=True)
                        try:
                            ret = func(self, *args, **kwargs)
                        except Exception as e:
                            logging.error(log_msg + f"Exception after lock failure, error: {e}", exc_info=True)
                            raise e
                        return ret
                    else:
                        logging.info(log_msg + f'Not executing after lock failure, error:{e}', exc_info=True)
                        raise e

                else:
                    # For other errors, release the lock and throw the exception
                    try:
                        self_locker.release()
                    except redis_lock.NotAcquired:
                        logging.info(log_msg + ' Lock released successfully')
                    # Release the other party's lock
                    try:
                        wait_for_locker.release()
                        logging.info(wait_log_msg + ' Released the other party\'s lock successfully')
                    except redis_lock.NotAcquired:
                        logging.info(wait_log_msg + ' Failed to release the other party\'s lock')

                    raise e

            return ret

        return wrapper

    return lock_func


def release_all_lock():
    # Clear locks when restarting the service to prevent deadlocks
    keys = BaseCache().connection.keys('lock*')
    for k in keys:
        BaseCache().connection.delete(k)


def lock_timed_task(func):
    """
    Allow the same function with the same parameters to execute only once within 60 seconds
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = f'lock:{func.__qualname__}:{args}:{kwargs}'
        if BaseCache().set(key, 1, nx=True, ex=EXPIRE):
            return func(self, *args, **kwargs)
        else:
            logging.info(f'{key} already exists within {EXPIRE} seconds')

    return wrapper


@contextmanager
def named_lock(name):
    """
    Named lock
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
            logging.error(f'Lock {name} has already been released')
