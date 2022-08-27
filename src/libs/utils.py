import os
import json
import time
import datetime
import dateutil.parser
import dateutil.tz
import pytz
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
            # Overwrite args if given any from requests
            if len(args):
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
        except (ImportError, AttributeError, ValueError) as e:
            logger.error(f"Importing module error {handler}: {e}")
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


def convert_ts_to_dt(timestamp):
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    dt = dateutil.parser.parse(timestamp)
    # Implicitly convert local timestamps to UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt


def convert_dt_to_ts(dt):
    if not isinstance(dt, datetime.datetime):
        print("Expected datetime, got %s" % (type(dt)))
        return dt
    ts = dt.isoformat()
    # Round microseconds to milliseconds
    if dt.tzinfo is None:
        # Implicitly convert local times to UTC
        return ts + "Z"
    # isoformat() uses microsecond accuracy and timezone offsets
    # but we should try to use millisecond accuracy and Z to indicate UTC
    return ts.replace("000+00:00", "Z").replace("+00:00", "Z")


def enrich_ts_to_dt_with_format(timestamp, ts_format):
    if isinstance(timestamp, datetime.datetime):
        return timestamp
    dt = datetime.datetime.strptime(timestamp, ts_format)
    # Implicitly convert local timestamps to UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dateutil.tz.tzutc())
    return dt


def enrich_dt_to_ts_with_format(dt, ts_format):
    if not isinstance(dt, datetime.datetime):
        print("Expected datetime, got %s" % (type(dt)))
        return dt
    ts = dt.strftime(ts_format)
    return ts


def ts_now():
    return datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())


def convert_ts_utc_to_tz(ts, tz_name):
    """Convert utc time to local time."""
    return ts.astimezone(dateutil.tz.gettz(tz_name))


def inc_ts(timestamp, milliseconds=1):
    """Increment a timestamp by milliseconds."""
    dt = convert_ts_to_dt(timestamp)
    dt += datetime.timedelta(milliseconds=milliseconds)
    return convert_dt_to_ts(dt)


def pretty_ts(timestamp, tz=True, ts_format=None):
    """Pretty-format the given timestamp (to be printed or logged hereafter).
    If tz, the timestamp will be converted to local time.
    Format: YYYY-MM-DD HH:MM TZ"""
    dt = timestamp
    if not isinstance(timestamp, datetime.datetime):
        dt = convert_ts_to_dt(timestamp)
    if tz:
        dt = dt.astimezone(dateutil.tz.tzlocal())
    if ts_format is None:
        return dt.strftime("%Y-%m-%d %H:%M %Z")
    else:
        return dt.strftime(ts_format)


def ts_add(ts, td):
    """Allows a timedelta (td) add operation on a string timestamp (ts)"""
    return convert_dt_to_ts(convert_ts_to_dt(ts) + td)
