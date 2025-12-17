import logging


def setup_logging(level="INFO", to_file=False, to_console=True, filename="app.log"):
    """Configure global logging."""
    handlers = []
    if to_console:
        handlers.append(logging.StreamHandler())
    if to_file:
        handlers.append(logging.FileHandler(filename, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="[%(levelname)s] %(asctime)s - %(message)s",
        handlers=handlers,
    )
