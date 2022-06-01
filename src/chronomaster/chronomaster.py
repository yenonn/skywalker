from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import json

# scheduler = BlockingScheduler()


# @scheduler.scheduled_job("interval", seconds=1)
# def job1():
#     print(f"job1: {datetime.now()}")


# @scheduler.scheduled_job("interval", seconds=2)
# def job2():
#     print(f"job2: {datetime.now()}")


# scheduler.start()


class JobRequest(object):
    def __init__(self, env):
        self.env = env
        self.schedules = Schedule(self.env).schedules
        self.requests = self.job_requests()

    def job_requests(self):
        job_requests = []
        for config in self.schedules:
            for key in config.keys():
                config_file = key
                job_name = str(config_file).replace("-config.json", "")
                job_requests.append(
                    {
                        "job_name": job_name,
                        "python-codes-config": config_file,
                        "python-codes-args": {},
                    }
                )
        return job_requests


class Schedule(object):
    def __init__(self, env):
        self.env = env
        self.function_configs = self.find_configs()
        self.schedules = self.find_schedules()

    def find_configs(self):
        path = os.getcwd()
        config_files = [f for f in os.listdir(path) if f.endswith("config.json")]
        return config_files

    def find_schedules(self):
        schedules = []
        for file in self.function_configs:
            with open(file) as jsonfile:
                data = json.load(jsonfile)
                for sched in data.get("schedule"):
                    if sched.get("environment") == self.env:
                        schedules.append({file: sched})
        return schedules
