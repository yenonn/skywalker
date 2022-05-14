import os
import time
import logging
from logging.config import dictConfig
from singleton import Singleton


class LoggerFactory(metaclass=Singleton):
    def __init__(self):
        self.LogLevel = "INFO"
        if os.getenv("LOG_LEVEL"):
            self.LogLevel = os.getenv("LOG_LEVEL")

        LOGGER = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-7s| [%(threadName)s] %(pathname)s:%(funcName)s:%(lineno)d | %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                }
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {"": {"handlers": ["stdout"], "level": f"{self.LogLevel}"}},
        }
        dictConfig(LOGGER)
        logging.Formatter.converter = time.gmtime
        self.Logger = logging.getLogger()
