from flask import Flask
from singleton import Singleton
import os


redis_cred = os.getenv("redis-password")


class FlaskFactory(metaclass=Singleton):
    def __init__(self):
        self.app = Flask("FlaskFactory")
        self.connect_redis = f"redis://default:{redis_cred}@redis-master:6379/0"
        self.app.config.update(
            CELERY_BROKER_URL=self.connect_redis,
            CELERY_RESULT_BACKEND=self.connect_redis,
        )
