from logger import LoggerFactory
from utils import check_dns, load_config, load_module, timeit
from abc import ABC, abstractmethod

logger = LoggerFactory().Logger


class AbstractExecutor(ABC):
    @abstractmethod
    def execute():
        raise NotImplementedError("Please implement this method")


class BaseExecutor(AbstractExecutor):
    def __init__(self):
        self.logger = LoggerFactory().Logger

    def execute(self):
        raise NotImplementedError("Please implement this method")

    def _loading_and_calling(self, handler):
        caller = load_module(handler)
        if caller:
            caller()
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
}
"""


class DefaultExecutor(BaseExecutor):
    def __init__(self, config):
        super().__init__()
        self.func_config = config

    @timeit
    def execute(self):
        name = self.func_config.get("name")
        handler = self.func_config.get("handler")
        self.logger.info(f"BaseExecutor function: {name}")
        super()._loading_and_calling(handler)


"""
WorkflowExecutor
The executor that accepts a series of handlers. It will run in the order of handler.
It accepts a config json object.
{
    "name": "workflow-skywalker",
    "executor": "executor.WorkflowExecutor",
    "handler": ["hello-skywalker.main", "workflow-skywalker.main"]
}
"""


class WorkflowExecutor(BaseExecutor):
    def __init__(self, config):
        super().__init__()
        self.func_config = config

    @timeit
    def execute(self):
        name = self.func_config.get("name")
        handlers = self.func_config.get("handler")
        self.logger.info(f"WorkflowExecutor function: {name}")
        for handler in handlers:
            super()._loading_and_calling(handler)


"""
ActivePassiveExecutor 
The extension from DefaultExecutor, which it will run based on the DNS/CNAME.
It accepts a config.json object.
{
    "name": "activepassive-hello-skywalker",
    "executor": "executor.ActivePassiveExecutor",
    "handler": "hello-skywalker.main"
}
"""


class ActivePassiveExecutor(DefaultExecutor):
    def __init__(self, config):
        super().__init__(config)
        self.func_config = config

    @timeit
    def execute(self):
        name = self.func_config.get("name")
        handler = self.func_config.get("handler")
        self.logger.info(f"ActivePassiveExecutor function: {name}")
        if check_dns():
            super().execute()
        else:
            self.logger.info(
                f"Skipping execution({handler}) due to current DNS/CNAME is not active"
            )


"""
ActivePassiveWorkflowExecutor
The executor that extends from WorkflowExecutor, which it will run based on the DNS/CNAME.
It accepts a config json object.
{
    "name": "activepassive-workflow-skywalker",
    "executor": "executor.ActivePassiveWorkflowExecutor",
    "handler": ["hello-skywalker.main", "workflow-skywalker.main"]
}
"""


class ActivePassiveWorkflowExecutor(WorkflowExecutor):
    def __init__(self, config):
        super().__init__(config)
        self.func_config = config

    @timeit
    def execute(self):
        name = self.func_config.get("name")
        handler = self.func_config.get("handler")
        self.logger.info(f"ActivePassiveWorkflowExecutor function: {name}")
        if check_dns():
            super().execute()
        else:
            self.logger.info(
                f"Skipping execution({handler}) due to current DNS/CNAME is not active"
            )


"""
 Main Entrypoint
"""


def main_entrypoint(config):
    func_config = load_config(config)
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
