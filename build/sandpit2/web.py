from flask_factory import FlaskFactory
from job_controller import run
from flask import request

flask_app = FlaskFactory().app


@flask_app.route("/execute", methods=["POST", "GET"])
def executor():
    print("Executing task ...")
    config = request.get_json()
    task = run.delay(**{"job_config": config})
    return f"task_id: {task.id}"


@flask_app.route("/healthz", methods=["GET"])
def healthz():
    return "ok"


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True)
