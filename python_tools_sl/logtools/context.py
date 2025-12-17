import logging
from contextlib import contextmanager


@contextmanager
def log_section(name: str):
    """Context manager to log entry/exit of a section."""
    logging.info(">>> Entering section: %s", name)
    try:
        yield
    finally:
        logging.info("<<< Exiting section: %s", name)
