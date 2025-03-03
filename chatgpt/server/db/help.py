#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 11:59
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 11:59
"""
import logging
import inspect
import os
import re
import pkgutil
from importlib import import_module
from peewee import Model
from peewee_migrate import Router, MigrateHistory, Migrator
from db import db
from functools import wraps
from psycopg2 import Error as pgError

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations')
IGNORE_MODELS = ['BaseModel', 'ResourceModel']


def sort_models(models):
    models = set(models)
    seen = set()
    ordering = list()

    def dfs(model):
        # peewee.sort_models 在 model in seen 这类相等判断时有迷之BUG，导致输出不对，这里采用 table_name 的判断
        if model._meta.table_name not in seen:
            seen.add(model._meta.table_name)
            for foreign_key, rel_model in model._meta.refs.items():
                if not foreign_key.deferred:
                    dfs(rel_model)
            if model._meta.depends_on:
                for dependency in model._meta.depends_on:
                    dfs(dependency)
            ordering.append(model)

    names = lambda m: (m._meta.name, m._meta.table_name)  # noqa: E731
    for m in sorted(models, key=names):
        dfs(m)
    return ordering


def get_tables(with_migration=False):
    tables = sort_models([
        m for m in load_models() if m.__name__ not in IGNORE_MODELS
    ])
    if with_migration:
        MigrateHistory.bind(db)
        tables.append(MigrateHistory)
    return tables


def load_models(package='models'):
    """读取所有模型"""

    if isinstance(package, str):
        package = import_module(package)

    models = []

    for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        module = import_module(name)
        models += [
            obj
            for _, obj in inspect.getmembers(
                module,
                lambda obj: isinstance(obj, type) and issubclass(obj, Model) and hasattr(obj, '_meta')
            )
        ]
        if is_pkg:
            models += load_models(module)
    return models


# def get_resource_models():
#     from . import ResourceModel
#     return [model for model in get_tables() if issubclass(model, ResourceModel)]


def drop_tables():
    for model in get_tables(True)[::-1]:
        model.drop_table(safe=True)


def create_tables(force=True):
    for model in get_tables(True):
        if force is True and model.table_exists():
            model.drop_table(safe=True)
        model.create_table(safe=True)


def truncate_tables(*args, **kwargs):
    for model in get_tables(True)[::-1]:
        if model.table_exists():
            model.truncate_table(*args, **kwargs)


def insert_init_data():
    print('插入初始化数据')
    try:
        with open('runtime/init.sql', 'r') as file:
            sql_script = file.read()
        db.execute_sql(sql_script)
    except Exception as e:
        print('插入初始化数据失败', e)
    else:
        print('插入初始化数据完成')


def initialize_db(force=True):
    if force:
        drop_tables()
    create_tables(force)
    load_exist_migrations()
    insert_init_data()


def migrate(router, name):
    MigrateHistory.bind(db)
    if not MigrateHistory.table_exists():
        logging.info("是初始化仓库，需要先创建表,正在创建表")
        initialize_db()
    else:
        logging.info("迁移记录已存在，执行增量迁移")
        migrator = Migrator(router.database)
        # 待迁移文件
        if not router.diff:
            logging.info('info, 无待迁移文件')
            return
        for diff in router.diff:
            logging.info(f'发现迁移文件{diff}')
            migrate_, _ = router.read(diff)
            migrate_(migrator, router.database)
            # 将更新操作分步骤执行
            ops = migrator.ops
            for op in ops:
                migrator.ops = [op]
                try:
                    migrator.run()
                except pgError as e:
                    # 字段重复
                    if e.pgcode == '42701':
                        logging.info(f'迁移文件{diff}: {e.pgerror},丢弃此次变更再执行')
                        # pg回滚事务
                        db.rollback()
                    else:
                        raise
            try:
                router.model.create(name=diff)
                logging.info(f'成功执行迁移文件{diff}')
            except pgError as e:
                # 主键重复，由于迁移表中数据与迁移文件差异导致，可以提交后再次尝试执行
                if e.pgcode == '23505':
                    logging.info(f'重试迁移文件{diff}')
                    db.commit()
                    router.model.create(name=diff)
                    logging.info(f'成功执行迁移文件{diff}')
            if name and name == diff:
                return


def rollback_migration(router, name):
    router.rollback(name)


def create_migration(router, name):
    router.create(name)


def get_router():
    return Router(db, migrate_dir=MIGRATIONS_DIR)


# 开启事务注解
def transaction(func):
    @wraps(func)
    def inner(*args, **kwargs):
        with db.atomic():
            return_value = func(*args, **kwargs)
            return return_value

    return inner


@transaction
def load_exist_migrations():
    filelist = os.listdir(MIGRATIONS_DIR)

    migrations = list()
    for f in filelist:
        if re.match(r'\d{3}_.*?\.py', f):
            migrations.append(f[:-3])
    MigrateHistory.bind(db)

    if not MigrateHistory.table_exists():
        MigrateHistory.create_table()

    for name in sorted(migrations):
        MigrateHistory.create(name=name)
