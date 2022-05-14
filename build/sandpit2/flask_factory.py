from flask import Flask
from singleton import Singleton


class FlaskFactory(metaclass=Singleton):
    def __init__(self):
        self.app = Flask("FlaskFactory")
        self.app.config.update(
            CELERY_BROKER_URL="redis://default:CvmvLA9aBT@redis-master:6379/0",
            CELERY_RESULT_BACKEND="redis://default:CvmvLA9aBT@redis-master:6379/0",
        )
