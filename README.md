# Skywalker
## Notice
This is a python framework to host python functions(Faas) in kubernetes environment. Skywalker is making use of celery and flask framework to achieve the goal. Here is the architecture diagram showing the high level overview of the project. 

![Alt text](docs/images/skywalker.drawio.png)

## Getting Started
### Prerequisite
* minikube
* docker
* Helm
### Setup
* Create your minikube cluster. Considering the base requirement of a minikube cluster, you can simply `minikube start` to create a kubernetes cluster locally.
* You have to do a redis cluster by running command. `helm install redis bitnami/redis`. Then monitor the redis pod until pod are fully up and running.
* Before you can go ahead and compile the docker image, please make sure that you are using the registr from minikube `eval $(minikube docker-env)`.
* Once all setup, you can start working on your image. Go to `build/images` directory, and you will find three base images.
* At once, please go into each image and run `./build.sh`.
* At last, you will have three different images, namely, `skywalker/python`, `skywalker/unzip`, `skywalker/core`.
* At `build/k8s`, you will find all the kubernetes yaml files for `skywalker-chronomaster`, `skywalker-executor` and `skywalker-proxy`.
* All of your function codes are located at `src/functions`. Thy are are examples that you can refer to e.g `hello-skywalker`.
* Before starting skywalker, you have to load the function codes onto a configmap. By that, you need to go to `tool` directory and run the `./buildcm.sh`. 
* With that, it will find all the python codes with src directory and load them onto a configmap, namely `python-configmap-codes`.
* Once you are done, now you can start skywalker, go to `tool` directory and run `run_skywalker.sh`.
### Q&A
* From the architecture point of view, `skywalker-chronomaster` acts as the trigger. It reads the `schedule` option derived from each function config.json file.
* By then, it submits an async HTTP request to `skywalker-proxy`. `skywalker-proxy` receives the request and submit a `celery` task and persists onto backend redis.
* With all the tasks pending, celery will schedule and `skywalker-executor` to run function as per defines from the function config.json.
* Each function comes with a config.json files. For reference, you can look at this `src/functions/hello-skywalker/hello-skywalker-config.json`
* `handler` and `args` working in pairs. `handler` is a list of function entry point, whereas `args` is the argument list that passed into a function.
* The options to control how to run a function is self-explanatory. 
* There are types of executors to run function, namely `executor.DefaultExecutor`, `executor.WorkflowExecutor`, `executor.ActivePassiveExecutor`, and `executor.ActivePassiveWorkflowExecutor`.
* `schedule` defines that interval of function executor, and it is scheduled in `@every` syntax at certain second `s`, minute `m` and hour `h`
* `enabled` is a toggle to enable and disable a function from scheduled and execute.
## Contributors
This projects exists thanks to all the people who contributed. 
<a href="https://github.com/yenonn/skywalker/contributors">here</a>
