from apscheduler.schedulers.blocking import BlockingScheduler
import os
import json
import requests


class Chronomaster(object):
    url = "http://skywalker-proxy:5000/execute"

    def __init__(self):
        self.env = os.getenv("Environment")
        self.sched = BlockingScheduler()
        self.job_requests = JobRequest(self.env).requests

    def _trigger(self, data):
        requests.post(self.url, data=data, headers={"Content-Type": "Application/json"})

    def jobs(self):
        for config, job in self.job_requests.items():
            print(f"Fetching job - {config}")
            yield job

    def add_jobs(self):
        for job in self.jobs():
            cron = job.get("cron")
            job.pop("environment")
            self.sched.add_job(self._trigger, "interval", [job], seconds=5)

    def start(self):
        self.sched.start()

    def stop(self):
        self.sched.shutdown()

    def pause(self):
        self.sched.pause()

    def resume(self):
        self.sched.resume()


class JobRequest(object):
    def __init__(self, env):
        self.env = env
        self.schedules = Schedule(self.env).schedules
        self.requests = self.job_requests()

    def job_requests(self):
        job_requests = {}
        for config, schedule in self.schedules.items():
            job_name = str(config).replace("-config.json", "")
            job = {
                "job_name": job_name,
                "python-codes-config": config,
                "python-codes-args": {},
            }
            job_requests[config] = {**job, **schedule}

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
        schedules = {}
        for file in self.function_configs:
            with open(file) as jsonfile:
                data = json.load(jsonfile)
                for sched in data.get("schedule"):
                    if sched.get("environment") == self.env:
                        schedules[file] = sched
        return schedules
