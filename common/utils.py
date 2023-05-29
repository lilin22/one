import json,os,time
import traceback
from functools import wraps
from common.configLog import logger

def catch_exception(func):
    """捕获异常写入日志"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise Exception(logger.error(traceback.format_exc()))
    return wrapper

class singleton:
    _instance = None
    instance = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._isnstance
