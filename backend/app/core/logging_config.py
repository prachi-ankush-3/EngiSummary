"""
Logging Configuration Module
Sets up logging for the application
"""

import logging
import logging.config
from app.core.config import settings


def configure_logging():
    """Configure logging for the application"""
    
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "detailed",
                "filename": "app.log"
            },
        },
        "loggers": {
            "app": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file"]
            },
            "uvicorn": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"]
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"]
        }
    }
    
    logging.config.dictConfig(log_config)
    return logging.getLogger("app")


# Create logger instance
logger = configure_logging()
