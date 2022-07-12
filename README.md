# Skywalker
## Notice
This is a python framework to host python functions(Faas) in kubernetes environment. Skywalker is making use of celery and flask framework to achieve the goal. Here is the architecture diagram showing the high level overview of the project. 

![Alt text](docs/images/skywalker.drawio.png)

## Getting Started
### Prerequisite
* minikube
* docker
### Setup
* Create your minikube cluster. Considering the base requirement of a minikube cluster, you can simply `minikube start` to create a kubernetes cluster locally.
* Before you can go ahead and compile the docker image, please make sure that you are using the registr from minikube `eval $(minikube docker-env)`
* Once all setup, you can start working on your image. Go to build/images directory, and you will find three base images
* At once, please go into each image and run `./build.sh`
* At last, you will have three different images, namely, `skywalker/python`, `skywalker/unzip`, `skywalker/core`
* All of your function codes are located at `src/functions`. Thy are are examples that you can refer to e.g `hello-skywalker`
* Before starting skywalker, you have to load the function codes onto a configmap. By that, you need to go to `tools` directory and run the `./buildcm.sh` 
* With that, it will find all the python codes with src directory and load them onto a configmap, namely `python-configmap-codes`
* Once you are done, now you can start skywalker, go to `tools` directory and run `run_skywalker.sh`
### Q&A
* Each function comes with a config.json files. For reference, you can look at this `src/functions/hello-skywalker/hello-skywalker-config.json`
* The options to control how to run a function is self-explanatory. 
* There are types of executors: `executor.DefaultExecutor`, `executor.WorkflowExecutor`, `executor.ActivePassiveExecutor`, and `executor.ActivePassiveWorkflowExecutor`.
* `schedule` defines that interval of function executor, and it is scheduled in `@every` syntax at certain second `s`, minute `m` and hour `h`
* `enabled` is a toggle to enable and disable a function from scheduled and execute.
## Contributors
This projects exists thanks to all the people who contributed. 
<a href="https://github.com/yenonn/skywalker/contributors">here</a>
