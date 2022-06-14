from apscheduler.schedulers.blocking import BlockingScheduler
import os
import json
import requests


class Chronomaster(object):
    url = "http://localhost:5000/execute"

    def __init__(self):
        self.env = os.getenv("Environment")
        self.sched = BlockingScheduler()
        self.job_requests = JobRequest(self.env).requests
        self.add_jobs()

    def _trigger(self, data):
        requests.post(
            self.url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def jobs(self):
        for config, job in self.job_requests.items():
            yield job

    def add_jobs(self):
        for job in self.jobs():
            cron_args = CronParser(job.get("cron")).parse()
            trigger_args = {"func": self._trigger, "kwargs": {"data": job}}
            job_args = {**cron_args, **trigger_args}
            self.sched.add_job(**job_args)

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
            job = {"job-name": job_name, "python-codes-config": config}
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
            with open(file) as jsonfile:
                data = json.load(jsonfile)
                for sched in data.get("schedule"):
                    if sched.get("environment") == self.env:
                        schedules[file] = sched
        return schedules
