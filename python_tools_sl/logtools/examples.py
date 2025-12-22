from typing import Any

from .config import setup_logging
from .context import log_section
from .decorators import log_call

# from outside :just do : from logging import setup_logging, log_call, log_section

setup_logging(level="DEBUG")


@log_call
def add(a: Any, b: Any) -> Any:
    return a + b


with log_section("Demo ADD"):
    add(2, 3)
