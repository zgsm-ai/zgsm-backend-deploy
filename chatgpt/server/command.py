#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from flask.cli import FlaskGroup
from app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    click.echo('===> chatGpt server')


@cli.command()
@click.option('--force/--unforce', default=False)
def initdb(force):
    """Initialize database"""
    from db.help import initialize_db
    initialize_db(force)
    click.echo('Database initialization successful')


@cli.command()
def dropdb():
    """delete all tables"""
    from db.help import drop_tables
    drop_tables()
    click.echo('Database table deletion successful')


@cli.command()
def cleardb():
    """clear data"""
    from db.help import truncate_tables
    truncate_tables()
    click.echo('Database clear successful')


@cli.command()
@click.option('--name', help='migration name')
def create_migration(name):
    """Create migration file"""
    from db.help import get_router, create_migration
    router = get_router()
    create_migration(router, name)


@cli.command()
@click.option('--name', help='migration name')
def migrate(name):
    """migrate database"""
    from db.help import get_router, migrate
    router = get_router()
    migrate(router, name)

@cli.command()
@click.option('--name', help='insert_advice_prompt')
def insert_advice_prompt(name):
    from scripts.add_advcie_prompt_configuration import AddAdvicePrompt
    AddAdvicePrompt.run()

@cli.command()
@click.option('--name', help='clear_all_prompt_template_cache')
def clear_prompt_cache(name):
    # python command.py clear-prompt-cache Cached prompt template emptied
    pass

if __name__ == "__main__":
    cli()
