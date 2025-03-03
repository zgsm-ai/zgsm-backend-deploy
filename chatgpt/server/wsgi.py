"""
For wsgi server
"""
from logger import setup_logging
from app import create_app

setup_logging()
app = create_app()
