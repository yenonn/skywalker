from apscheduler.schedulers.background import BackgroundScheduler
from singleton import Singleton
import os
import json
import requests


class Chronomaster(metaclass=Singleton):
    url = "http://proxy-service:5000/execute"

    def __init__(self):
        self.env = os.getenv("environment")
        self.sched = BackgroundScheduler()
        self.job_requests = JobRequest(self.env).requests
        self.add_jobs()
        if not self.sched.running:
            self.sched.start()
            self.sched.get_jobs()

    def _trigger(self, data):
        requests.post(
            self.url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def get_job_details(self):
        jobs_details = []
        for config in self.job_requests.keys():
            with open(config) as config_file:
                data = json.load(config_file)
                jobs_details.append(data)
        return jobs_details

    def add_jobs(self):
        for _, job in self.job_requests.items():
            cron_args = CronParser(job.get("cron")).parse()
            trigger_args = {
                "func": self._trigger,
                "kwargs": {"data": job},
                "id": job.get("job-name"),
            }
            job_args = {**cron_args, **trigger_args}
            self.sched.add_job(**job_args)

    def stop(self):
        if self.state() == "running":
            self.sched.pause()

    def start(self):
        if self.state() == "stop":
            self.sched.resume()

    def state(self):
        state = {0: "idle", 1: "running", 2: "stop"}
        return state.get(self.sched.state)


class JobRequest(object):
    def __init__(self, env):
        self.env = env
        self.schedules = Schedule(self.env).schedules
        self.requests = self.job_requests()

    def job_requests(self):
        job_requests = {}
        for config, schedule in self.schedules.items():
            job_name = str(config).replace("-config.json", "")
            job = {"job-name": job_name}
            job_requests[config] = {**job, **schedule}

        return job_requests


class CronParser(object):
    def __init__(self, cron_string):
        self.cron = str(cron_string).strip().split()

    def parse(self):
        time_interval = self.cron[-1]
        trigger_type = self.cron[0]
        parse_return = {}
        if str(trigger_type).startswith("@every"):
            parse_return["trigger"] = "interval"

        if str(time_interval).endswith("s"):
            # seconds
            time_value = int(time_interval.replace("s", ""))
            parse_return["seconds"] = time_value
        elif str(time_interval).endswith("m"):
            # minutes
            time_value = int(time_interval.replace("m", ""))
            parse_return["minutes"] = time_value
        elif str(time_interval).endswith("h"):
            # hours
            time_value = int(time_interval.replace("h", ""))
            parse_return["hours"] = time_value
        return parse_return


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
            schedule_details = {}
            schedule_details["python-codes-config"] = file
            with open(file) as jsonfile:
                data = json.load(jsonfile)
                if data.get("args"):
                    schedule_details["python-codes-args"] = data.get("args")
                for sched in data.get("schedule"):
                    if sched.get("environment") == self.env:
                        schedule_details.update(sched)
            schedules[file] = schedule_details
        return schedules
