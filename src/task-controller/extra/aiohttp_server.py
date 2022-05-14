from aiohttp import web
from k8s_job_controller import Job


async def execute(request):
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    config = {
        "namespace": "default",
        "job-name": "hello-skywalker",
        "python-codes-configmap-name": "hello-skywalker-configmap",
    }

    k8s_job = Job(job_config=config)
    k8s_job.run()
    return web.Response(text=text)


async def healthz(request):
    return web.Response(text="ok")


app = web.Application()
app.add_routes([web.get("/execute", execute), web.get("/healthz", healthz)])

if __name__ == "__main__":
    web.run_app(app)
