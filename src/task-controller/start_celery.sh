celery -A job_controller.app worker --loglevel=info -n worker-$HOSTNAME

