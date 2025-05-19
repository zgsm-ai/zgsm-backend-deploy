import logging
import os
import sys
from logging.handlers import RotatingFileHandler
import json

# Define color codes for console output
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m', # Yellow
        'ERROR': '\033[91m',   # Red
        'CRITICAL': '\033[91m\033[1m', # Bold Red
        'RESET': '\033[0m'    # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        if record.levelname in self.COLORS and sys.stderr.isatty():
            return f"{self.COLORS[record.levelname]}{log_message}{self.COLORS['RESET']}"
        return log_message

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_record)

# Get log level from environment variable or default to INFO
log_level_name = os.environ.get('LOG_LEVEL', 'INFO')
log_level = getattr(logging, log_level_name.upper(), logging.INFO)

# Get log format from environment variable
log_format = os.environ.get('LOG_FORMAT', 'standard')  # standard or json

# Configure logger
logger = logging.getLogger("fauxpilot")

# Remove existing handlers to prevent duplicates
if logger.hasHandlers():
    logger.handlers.clear()

# Create console handler
console_handler = logging.StreamHandler()

# Set formatter based on format type
if log_format.lower() == 'json':
    formatter = JsonFormatter()
else:
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(log_level)

# Propagate logs to root logger to ensure logs appear in container logs
logger.propagate = True 