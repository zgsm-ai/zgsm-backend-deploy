#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Su Deli 16646
    :Time: 2023/3/14 11:59
    :Modifier: Su Deli 16646
    :UpdateTime: 2023/3/14 11:59
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
        # peewee.sort_models has a mysterious BUG in equality judgment such as model in seen, which leads to incorrect output. Here, the table_name judgment is used
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
    """Read all models"""

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
    print('Insert initialization data')
    try:
        with open('runtime/init.sql', 'r') as file:
            sql_script = file.read()
        db.execute_sql(sql_script)
    except Exception as e:
        print('Failed to insert initialization data', e)
    else:
        print('Initialization data insertion completed')


def initialize_db(force=True):
    if force:
        drop_tables()
    create_tables(force)
    load_exist_migrations()
    insert_init_data()


def migrate(router, name):
    MigrateHistory.bind(db)
    if not MigrateHistory.table_exists():
        logging.info("It is the initialization warehouse, you need to create a table first, and the table is being created")
        initialize_db()
    else:
        logging.info("Migration record already exists, performing incremental migration")
        migrator = Migrator(router.database)
        # Migration file to be migrated
        if not router.diff:
            logging.info('info, no migration file to be migrated')
            return
        for diff in router.diff:
            logging.info(f'Found migration file{diff}')
            migrate_, _ = router.read(diff)
            migrate_(migrator, router.database)
            # Perform update operations in steps
            ops = migrator.ops
            for op in ops:
                migrator.ops = [op]
                try:
                    migrator.run()
                except pgError as e:
                    # Field duplicate
                    if e.pgcode == '42701':
                        logging.info(f'Migration file{diff}: {e.pgerror}, discard this change and execute again')
                        # pg rollback transaction
                        db.rollback()
                    else:
                        raise
            try:
                router.model.create(name=diff)
                logging.info(f'Successfully executed migration file{diff}')
            except pgError as e:
                # Primary key is duplicated, which is caused by the difference between the data in the migration table and the migration file. You can submit it and try to execute it again
                if e.pgcode == '23505':
                    logging.info(f'Retry migration file{diff}')
                    db.commit()
                    router.model.create(name=diff)
                    logging.info(f'Successfully executed migration file{diff}')
            if name and name == diff:
                return


def rollback_migration(router, name):
    router.rollback(name)


def create_migration(router, name):
    router.create(name)


def get_router():
    return Router(db, migrate_dir=MIGRATIONS_DIR)


# Enable transaction annotation
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
