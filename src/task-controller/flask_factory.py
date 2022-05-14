from flask import Flask
from singleton import Singleton
import os


class FlaskFactory(metaclass=Singleton):
    def __init__(self):
        redis_cred = os.getenv("REDIS_CREDENTIAL")
        self.app = Flask("FlaskFactory")
        self.app.config.update(
            CELERY_BROKER_URL=f"redis://default:{redis_cred}@redis-master:6379/0",
            CELERY_RESULT_BACKEND="redis://default:{redis_cred}@redis-master:6379/0",
        )
