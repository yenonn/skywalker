import uuid
from celery_factory import CeleryFactory
from flask_factory import FlaskFactory
from logger import LoggerFactory
from executor import main_entrypoint

# This is the celery worker
app = CeleryFactory(FlaskFactory().app).app
logger = LoggerFactory().Logger


@app.task(retries=3)
def run(job_config):
    python_config = job_config.get("python-codes-config")
    job_name = f"job-{job_config.get('job-name')}-{uuid.uuid4().hex}"
    logger.info(f"***Executing {job_name}***")
    try:
        main_entrypoint(python_config)
    except Exception as e:
        logger.error(f"Error executing function: {e}")
    logger.info(f"***Job {job_name} completed.***")
