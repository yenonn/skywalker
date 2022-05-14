import os
import json
import time
import socket
from importlib import import_module
from logger import LoggerFactory

logger = LoggerFactory().Logger

"""
Loading the modules from config.json
"""


def load_config(config):
    func_config = {}
    if os.path.isfile(config):
        with open(config) as jsonfile:
            func_config = json.load(jsonfile)
    else:
        raise Exception("No /app/config.json found. Module loading is not possible.")
    return func_config


"""
Loading the given handler caller
"""


def load_module(handler):
    caller = None
    if handler:
        pathname = ".".join(handler.split(".")[:-1])
        name = handler.split(".")[-1]
        try:
            module = import_module(pathname)
            caller = getattr(module, name)
        except ImportError as e:
            logger.error(f"Importing module error: {e}")
    return caller


"""
Decorator to time function
"""


def timeit(func):
    def wrapper_func(self, *args, **kwargs):
        start = time.perf_counter()
        func(self, *args, **kwargs)
        elapsed_time = time.perf_counter() - start
        logger.info(f"Total execution time: {elapsed_time:0.4f} seconds ")

    return wrapper_func


"""
Detecting the DNS/CNAME APP_ENDPOINT which one is active 
return True/False
"""


def check_dns():
    app_endpoint = os.getenv("APP_ENDPOINT")
    if socket.gethostbyname_ex(app_endpoint):
        pass
    return False
