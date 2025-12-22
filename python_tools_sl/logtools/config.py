import logging


def setup_logging(
    level: str = "INFO", to_file: bool = False, to_console: bool = True, filename: str = "app.log"
) -> None:
    """Configure global logging."""
    handlers: list[logging.Handler] = []
    if to_console:
        handlers.append(logging.StreamHandler())
    if to_file:
        handlers.append(logging.FileHandler(filename, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="[%(levelname)s] %(asctime)s - %(message)s",
        handlers=handlers,
    )
