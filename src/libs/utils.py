import os
import json
import time
import socket
from importlib import import_module
from logger import LoggerFactory
from envparse import env

logger = LoggerFactory().Logger

"""
Loading the modules from config.json
Merging it with given args
"""


def load_config(config, args):
    func_config = {}
    config_file = f"/app/{config}"
    if os.path.isfile(config_file):
        with open(config_file) as jsonfile:
            func_config = json.load(jsonfile)
            func_config["args"] = args
    else:
        raise Exception("No /app/config.json found. Module loading is not possible.")
    return func_config


"""
Loading the given handler caller
"""


def load_module(handler: str):
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
    return False


"""
Reading value from .env file or environment by given the key
"""


def config(key: str):
    if os.path.exists(".env"):
        env.read_envfile()
        return env(key)
    if os.getenv(key):
        return os.getenv(key)
