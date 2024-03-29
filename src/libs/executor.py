from logger import LoggerFactory
from utils import check_dns, load_config, load_module, timeit
from abc import ABC, abstractmethod

logger = LoggerFactory().Logger


class AbstractExecutor(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Please implement this method")


class BaseExecutor(AbstractExecutor):
    def __init__(self):
        self.logger = LoggerFactory().Logger

    def execute(self):
        raise NotImplementedError("Please implement this method")

    def _loading_and_calling(self, handler, args):
        caller = load_module(handler)
        if caller:
            caller(**args)
        else:
            logger.error("No handler is loaded and running.")

    def _prometheus(self):
        pass

    def _metrics(self):
        pass


"""
DefaultExecutor 
The most basic executor where it is hit and run. 
It accepts a config.json object.
{
    "name": "hello-skywalker",
    "executor": "executor.DefaultExecutor",
    "handler": "hello-skywalker.main"
    "args": {}
}
"""


class DefaultExecutor(BaseExecutor):
    def __init__(self, config):
        super().__init__()
        self.func_config = config
        self.name = self.func_config.get("name")
        self.handler = self.func_config.get("handler")
        self.args = self.func_config.get("args")
        self.enabled = self.func_config.get("enabled")

    @timeit
    def execute(self):
        self.logger.info(f"BaseExecutor function: {self.name}")
        if self.enabled:
            super()._loading_and_calling(self.handler, self.args)
        else:
            self.logger.warn(f"Function {self.name} is disabled.")


"""
WorkflowExecutor
The executor that accepts a series of handlers. It will run in the order of handler.
It accepts a config json object.
{
    "name": "workflow-skywalker",
    "executor": "executor.WorkflowExecutor",
    "handler": ["hello-skywalker.main", "workflow-skywalker.main"] 
    "args": [{}, {}]
}
"""


class WorkflowExecutor(BaseExecutor):
    def __init__(self, config):
        super().__init__()
        self.func_config = config
        self.name = self.func_config.get("name")
        self.handlers = self.func_config.get("handler")
        self.args = self.func_config.get("args")
        self.enabled = self.func_config.get("enabled")

    @timeit
    def execute(self):
        self.logger.info(f"WorkflowExecutor function: {self.name}")
        if self.enabled:
            for (handler, arg) in zip(self.handlers, self.args):
                self.logger.info(f"WorkflowExecutor function: {self.name}")
                super()._loading_and_calling(handler, arg)
        else:
            self.logger.warn(f"Function {self.name} is disabled.")


"""
ActivePassiveExecutor 
The extension from DefaultExecutor, which it will run based on the DNS/CNAME.
It accepts a config.json object.
{
    "name": "activepassive-hello-skywalker",
    "executor": "executor.ActivePassiveExecutor",
    "handler": "hello-skywalker.main"
    "args": {}
}
"""


class ActivePassiveExecutor(DefaultExecutor):
    def __init__(self, config):
        self.func_config = config
        super().__init__(config)
        self.name = self.func_config.get("name")
        self.handler = self.func_config.get("handler")
        self.args = self.func_config.get("args")
        self.enabled = self.func_config.get("enabled")

    @timeit
    def execute(self):
        self.logger.info(f"ActivePassiveExecutor function: {self.name}")
        if self.enabled:
            if check_dns():
                super().execute()
            else:
                self.logger.info(
                    f"Skipping execution({self.handler}) due to current DNS/CNAME is not active"
                )
        else:
            self.logger.warn(f"Function {self.name} is disabled.")


"""
ActivePassiveWorkflowExecutor
The executor that extends from WorkflowExecutor, which it will run based on the DNS/CNAME.
It accepts a config json object.
{
    "name": "activepassive-workflow-skywalker",
    "executor": "executor.ActivePassiveWorkflowExecutor",
    "handler": ["hello-skywalker.main", "workflow-skywalker.main"]
    "args": [{}, {}]
}
"""


class ActivePassiveWorkflowExecutor(WorkflowExecutor):
    def __init__(self, config):
        self.func_config = config
        super().__init__(config)
        self.name = self.func_config.get("name")
        self.handler = self.func_config.get("handler")
        self.args = self.func_config.get("args")
        self.enabled = self.func_config.get("enabled")

    @timeit
    def execute(self):
        self.logger.info(f"ActivePassiveWorkflowExecutor function: {self.name}")
        if self.enabled:
            if check_dns():
                super().execute()
            else:
                self.logger.info(
                    f"Skipping execution({self.handler}) due to current DNS/CNAME is not active"
                )
        else:
            self.logger.warn(f"Function {self.name} is disabled.")


"""
Main Entrypoint
Accepting sample of configuration from incoming calls
DefaultExecutor
 {
    "job-name": "hello-skywalker",
    "python-codes-config": "hello-skywalker-config.json" 
    "python-codes-args": {}
 }

WorkflowExecutor

 {
    "job-name": "workflow-skywalker",
    "python-codes-config": "workflow-skywalker-config.json" 
    "python-codes-args": [{}, {}]
 }
"""


def main_entrypoint(python_codes_config, python_codes_args):
    func_config = load_config(python_codes_config, python_codes_args)
    executor_name = func_config.get("executor")
    logger.info(f"Executor: {executor_name}")
    try:
        executor_cls = load_module(executor_name)
        if executor_cls:
            executor_obj = executor_cls(func_config)
            executor_obj.execute()
        else:
            logger.error("Executor is not loaded and running.")
    except Exception as e:
        logger.error(f"Main Entrypoint exception: {e}")
