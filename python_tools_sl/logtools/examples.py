from .config import setup_logging
from .decorators import log_call
from .context import log_section

# from outside :just do : from logging import setup_logging, log_call, log_section

setup_logging(level="DEBUG")


@log_call
def add(a, b):
    return a + b


with log_section("Demo ADD"):
    print(add(2, 3))
