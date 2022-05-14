from celery import Celery, Task
from singleton import Singleton
import sys, os


class CeleryFactory(metaclass=Singleton):
    """
    Accepting a flask application
    """

    def __init__(self, flask_app):
        sys.path.append(os.getcwd())
        self.app = Celery(
            flask_app.import_name,
            result_backend=flask_app.config["CELERY_RESULT_BACKEND"],
            broker=flask_app.config["CELERY_BROKER_URL"],
            result_expires=3600,
        )
        self.app.conf.update(flask_app.config)

        class ContextTask(Task):
            def __call__(self, *args, **kwargs):
                with flask_app.app_context():
                    return self.run(*args, **kwargs)

        self.app.Task = ContextTask
