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
    click.echo('Database initialized successfully')


@cli.command()
def dropdb():
    """Delete all tables"""
    from db.help import drop_tables
    drop_tables()
    click.echo('Database tables deleted successfully')


@cli.command()
def cleardb():
    """Clear data"""
    from db.help import truncate_tables
    truncate_tables()
    click.echo('Database cleared successfully')


@cli.command()
@click.option('--name', help='migration name')
def create_migration(name):
    """Create new migration file"""
    from db.help import get_router, create_migration
    router = get_router()
    create_migration(router, name)


@cli.command()
@click.option('--name', help='migration name')
def migrate(name):
    """Migrate database"""
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
    # python command.py clear-prompt-cache - Clear cached prompt templates
    pass

if __name__ == "__main__":
    cli()
