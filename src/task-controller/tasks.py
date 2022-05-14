from celery_factory import CeleryFactory
from flask_factory import FlaskFactory

flask_app = FlaskFactory().app
worker = CeleryFactory(flask_app).app


@worker.task()
def execute_test():
    print("worker is working hard....")
