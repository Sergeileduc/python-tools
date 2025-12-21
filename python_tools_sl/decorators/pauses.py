import asyncio
import time
from functools import wraps
from typing import Awaitable, Callable, Optional

from python_tools_sl.utils.typing_helpers import AsyncDecorator, Decorator, P, R


def with_pause(seconds: int | float = 2, message: Optional[str] = None) -> Decorator:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            print(message or f"⏸️ Pause de {seconds}s pour éviter les timeouts...")
            time.sleep(seconds)
            return result

        return wrapper

    return decorator


def with_pause_async(seconds: int | float = 2, message: Optional[str] = None) -> AsyncDecorator:
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = await func(*args, **kwargs)
            print(message or f"⏸️ Pause de {seconds}s pour éviter les timeouts...")
            await asyncio.sleep(seconds)
            return result

        return wrapper

    return decorator
