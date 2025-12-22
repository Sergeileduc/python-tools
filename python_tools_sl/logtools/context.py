import logging
from contextlib import contextmanager
from typing import Generator


@contextmanager
def log_section(name: str) -> Generator[None, None, None]:
    """Context manager to log entry/exit of a section."""
    logging.info(">>> Entering section: %s", name)
    try:
        yield
    finally:
        logging.info("<<< Exiting section: %s", name)
