from k8s_job_controller import Job as k8sjob
from job_controller import run
from celery import Celery, Task
from flask import Flask
import os


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


redis_cred = os.getenv("redis-password")
flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL=f"redis://default:{redis_cred}@redis-master:6379/0",
    CELERY_RESULT_BACKEND=f"redis://default:{redis_cred}@redis-master:6379/0",
)
celery = make_celery(flask_app)


@celery.task()
def execute_k8s_jobs():
    print("hello world, celery!")
    config = {
        "job-name": "hello-skywalker",
        "namespace": "default",
        "python-codes-configmap-name": "hello-skywalker-configmap",
    }
    k8s_job = k8sjob(config)
    k8s_job.run()


@celery.task()
def execute_local_jobs():
    print("hello world, celery!")
    config = {
        "job-name": "hello-skywalker",
        "python-codes-config": "hello-skywalker-config.json",
    }
    run(config)


@flask_app.route("/execute")
def execute():
    print("hello world, flask!")
    task = execute_k8s_jobs.delay()
    return f"task_id: {task.id}"


if __name__ == "__main__":
    flask_app.run(debug=True)
