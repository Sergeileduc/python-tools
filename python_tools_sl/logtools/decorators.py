import logging
from functools import wraps
from typing import Callable

from python_tools_sl.utils.typing_helpers import P, R


def log_call(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to log function calls and return values."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logging.debug("Calling %s with args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logging.debug("%s returned %s", func.__name__, result)
        return result

    return wrapper
