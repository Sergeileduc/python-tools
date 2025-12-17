import time
import asyncio
from functools import wraps


def with_pause(seconds=2.0, message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(message or f"⏸️ Pause de {seconds}s pour éviter les timeouts...")
            time.sleep(seconds)
            return result

        return wrapper

    return decorator


def with_pause_async(seconds=2.0, message=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            print(message or f"⏸️ Pause de {seconds}s pour éviter les timeouts...")
            await asyncio.sleep(seconds)
            return result

        return wrapper

    return decorator
