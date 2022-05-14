from flask import Flask, config
from singleton import Singleton
from utils import config


redis_cred = config("REDIS_CREDENTIAL")


class FlaskFactory(metaclass=Singleton):
    def __init__(self):
        self.app = Flask("FlaskFactory")
        self.app.config.update(
            CELERY_BROKER_URL=f"redis://default:{redis_cred}@redis-master:6379/0",
            CELERY_RESULT_BACKEND="redis://default:{redis_cred}@redis-master:6379/0",
        )
