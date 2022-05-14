from time import sleep
from kubernetes import client, config as conf
import uuid


class Job(object):
    def __init__(self, job_config):
        conf.load_config()
        self.job_successfully_completed = False
        self.app_vol = "app-volume"
        self.src_vol = "src-volume"
        self.app_mountpath = "/app"
        self.src_mountpath = "/src"
        self.job_config = job_config
        self.python_configmap = self.job_config.get("python-codes-configmap-name")
        self.job_name = f"job-{self.job_config.get('job-name')}-{uuid.uuid4().hex}"
        self.namespace = self.job_config.get("namespace")
        self.api = client.BatchV1Api()

    def job_object(self):
        # create volumes
        volume_app = client.V1Volume(
            name=self.app_vol, empty_dir=client.V1EmptyDirVolumeSource()
        )
        volume_src = client.V1Volume(
            name=self.src_vol,
            config_map=client.V1ConfigMapVolumeSource(name=self.python_configmap),
        )
        volume_app_mount = client.V1VolumeMount(
            name=self.app_vol, mount_path=self.app_mountpath
        )
        volume_src_mount = client.V1VolumeMount(
            name=self.src_vol, mount_path=self.src_mountpath
        )

        # create container and init-container
        app_container = client.V1Container(
            name="app",
            image="skywalker/python:0.1",
            command=["python", "/app/executor.py"],
            volume_mounts=[volume_app_mount],
        )

        init_container = client.V1Container(
            name="preparing-codes",
            image="skywalker/unzip:0.1",
            args=[
                "base64 -d < /src/code > /tmp/decoded && unzip -o /tmp/decoded -d /app"
            ],
            command=["sh", "-c"],
            volume_mounts=[volume_app_mount, volume_src_mount],
        )

        # build the template, spec, job
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "python-function"}),
            spec=client.V1PodSpec(
                restart_policy="Never",
                init_containers=[init_container],
                containers=[app_container],
                volumes=[volume_app, volume_src],
            ),
        )
        spec = client.V1JobSpec(template=template, backoff_limit=4)
        task = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=self.job_name),
            spec=spec,
        )

        return task

    def create_job(self):
        job = self.job_object()
        response = self.api.create_namespaced_job(body=job, namespace=self.namespace)
        print(f"Job: {self.job_name} is created.")

    def status(self):
        job_completed = False
        while not job_completed:
            response = self.api.read_namespaced_job_status(
                name=self.job_name, namespace=self.namespace
            )
            if (
                response.status.succeeded is not None
                or response.status.failed is not None
            ):
                job_completed = True
            sleep(1)
            print(f"Running {self.job_name}...")
            if response.status.succeeded:
                print(f"{self.job_name} is completed successfully.")
                self.job_successfully_completed = True
            if response.status.failed:
                print(f"{self.job_name} failed!")

    def delete_job(self):
        if self.job_successfully_completed:
            resp = self.api.delete_namespaced_job(
                name=self.job_name,
                namespace=self.namespace,
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5
                ),
            )

    def run(self):
        self.create_job()
        self.status()
        self.delete_job()


if __name__ == "__main__":
    config = {
        "namespace": "default",
        "job-name": "hello-skywalker",
        "python-codes-configmap-name": "hello-skywalker-configmap",
    }
    k8s_job = Job(job_config=config)
    k8s_job.run()
