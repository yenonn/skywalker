import os
import time
import logging
from datetime import datetime, timedelta
from logging.config import dictConfig


class DedupFilter(logging.Filter):
    def __init__(self, dedup_timeout: timedelta, name=""):
        super().__init__(name)
        self.dedup_timeout = dedup_timeout
        self.last_mg = None
        self.last_time = datetime(2022, 1, 1)

    def filter(self, record):
        now = datetime.now()
        should_dedup = (
            self.last_mg == record.msg and self.last_time + self.dedup_timeout > now
        )
        if should_dedup:
            return False
        else:
            self.last_mg = record.msg
            self.last_time = now
            return True


class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def logger_config(LogLevel="INFO"):
        if os.getenv("LOG_LEVEL"):
            LogLevel = os.getenv("LOG_LEVEL")

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
            "loggers": {"": {"handlers": ["stdout"], "Level": f"{LogLevel}"}},
        }
        dictConfig(LOGGER)
        logging.Formatter.converter = time.gmtime
        return logging.getLogger()
