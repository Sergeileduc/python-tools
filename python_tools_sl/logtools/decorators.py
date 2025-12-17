import logging
from functools import wraps


def log_call(func):
    """Decorator to log function calls and return values."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("Calling %s with args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logging.debug("%s returned %s", func.__name__, result)
        return result

    return wrapper
