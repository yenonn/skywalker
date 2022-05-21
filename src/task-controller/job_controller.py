import uuid
from celery_factory import CeleryFactory
from flask_factory import FlaskFactory
from logger import LoggerFactory
from executor import main_entrypoint

# This is the celery worker
app = CeleryFactory(FlaskFactory().app).app
logger = LoggerFactory().Logger

"""
Accepting sample of configuration from incoming calls
DefaultExecutor
 {
    "job-name": "hello-skywalker",
    "python-codes-config": "hello-skywalker-config.json" 
    "python-codes-args": {}
 }

WorkflowExecutor

 {
    "job-name": "workflow-skywalker",
    "python-codes-config": "workflow-skywalker-config.json" 
    "python-codes-args": [{}, {}]
 }
"""


@app.task(retries=3)
def run(job_config):
    job_name = f"job-{job_config.get('job-name')}-{uuid.uuid4().hex}"
    python_config = job_config.get("python-codes-config")
    python_args = job_config.get("python-codes-args", {})
    logger.info(f"***Executing {job_name}***")
    try:
        main_entrypoint(python_config, python_args)
    except Exception as e:
        logger.error(f"Error executing function: {e}")
    logger.info(f"***Job {job_name} completed.***")
