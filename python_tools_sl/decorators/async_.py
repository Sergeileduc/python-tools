import asyncio
import time
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type

from python_tools_sl.utils.formatting import format_duration
from python_tools_sl.utils.typing_helpers import AsyncDecorator, P, R


def with_pause_async(seconds: int | float = 2, message: Optional[str] = None) -> AsyncDecorator:
    """
    Décorateur async paramétrable qui ajoute une pause après l'exécution d'une fonction async.

    Ce décorateur est utile pour éviter les limitations de débit, les timeouts API,
    ou pour espacer volontairement des appels asynchrones successifs.

    Args:
        seconds (int | float, optionnel): Durée de la pause en secondes.
            Par défaut 2.
        message (str, optionnel): Message affiché avant la pause.
            Par défaut, un message générique indiquant la durée de la pause.

    Returns:
        AsyncDecorator: Un décorateur async qui peut être appliqué à une fonction async.

    Exemple:
        @with_pause_async(seconds=1.5)
        async def fetch_data(url: str) -> str:
            return await http_get(url)
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = await func(*args, **kwargs)
            print(message or f"⏸️ Pause de {seconds}s pour éviter les timeouts...")
            await asyncio.sleep(seconds)
            return result

        return wrapper

    return decorator


def timeit_async(prefix: str = "[ASYNC TIMEIT]") -> AsyncDecorator:
    """
    Décorateur async paramétrable qui mesure et affiche le temps d'exécution d'une fonction async.

    Ce décorateur est utile pour instrumenter des appels asynchrones, identifier des
    goulots d'étranglement, ou simplement obtenir une mesure précise du temps passé
    dans une coroutine.

    Args:
        prefix (str, optionnel): Texte affiché avant le nom de la fonction dans le log.
            Par défaut "[ASYNC TIMEIT]".

    Returns:
        AsyncDecorator: Un décorateur async qui peut être appliqué à une fonction async.

    Exemple:
        @timeit_async()
        async def foo():
            await asyncio.sleep(1)

        @timeit_async(prefix="[BENCH]")
        async def bar():
            await asyncio.sleep(1)
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{prefix} {func.__name__} exécutée en {format_duration(end - start)}")
            return result

        return wrapper

    return decorator


def retry_async(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> AsyncDecorator:
    """
    Décorateur async qui réessaie l'exécution d'une fonction async en cas d'exception.

    Ce décorateur est utile pour gérer des appels réseau instables, des opérations
    sensibles aux timeouts, ou toute coroutine susceptible d'échouer temporairement.

    Args:
        max_attempts (int): Nombre maximum de tentatives. Par défaut 3.
        delay (float): Délai en secondes entre deux tentatives. Par défaut 1.0.
        exceptions (Tuple[Type[Exception], ...]): Types d'exceptions qui déclenchent
            un nouvel essai. Par défaut, toutes les exceptions (`Exception`).

    Returns:
        AsyncDecorator: Un décorateur async qui peut être appliqué à une fonction async.

    Exemple:
        @retry_async(max_attempts=5, delay=0.5, exceptions=(ValueError,))
        async def fragile_func(x: int) -> int:
            if x < 0:
                raise ValueError("x doit être positif")
            return x * 2
    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"⚠️ Tentative {attempt}/{max_attempts} échouée : {e}")
                    if attempt < max_attempts:
                        await asyncio.sleep(delay)
            if last_exc is not None:
                raise last_exc
            raise RuntimeError("Échec du retry_async : aucune exception capturée")

        return wrapper

    return decorator


def memoize_async(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """
    Décorateur async qui met en cache les résultats d'une fonction async.

    Le cache est basé sur les arguments passés à la fonction. Les arguments doivent
    être hashables (ex. int, str, tuple). Ce décorateur est particulièrement utile
    pour optimiser des calculs récursifs ou des appels asynchrones répétitifs.

    Exemple:
        @memoize_async
        async def fib(n: int) -> int:
            return n if n < 2 else await fib(n - 1) + await fib(n - 2)
    """
    cache: Dict[tuple[Any, ...], R] = {}

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # clé basée sur args + kwargs (triés pour être hashables)
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        result = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


if __name__ == "__main__":
    import platform

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # TIMEIT
    @timeit_async()
    async def long(a: int, b: int) -> int:
        r = a + b
        await asyncio.sleep(1)
        return r

    # RETRY
    @retry_async(max_attempts=3, delay=0.5, exceptions=(ZeroDivisionError,))
    async def fragile_division(a: int, b: int) -> float:
        """Division qui peut échouer si b == 0"""
        return a / b

    # MEMOIZE
    @memoize_async
    async def fib(n: int) -> int:
        return n if n < 2 else await fib(n - 1) + await fib(n - 2)

    @timeit_async(prefix="[BENCH]")
    async def result_fib(n: int) -> int:
        return await fib(n)

    # MAIN
    async def main() -> None:
        print("TIMEIT---------------------")
        print(await long(1, 3))

        print("\nRETRY----------------------")
        try:
            print(f"résultat de la division {await fragile_division(10, 2)}")  # -> 5.0
            print(
                f"résultat de la division {await fragile_division(10, 0)}"
            )  # -> relance ZeroDivisionError après 3 tentatives
        except ZeroDivisionError:
            print("ok, Zero Division Error Impossible. Nombre d'essai max atteing")

        print("\nMEOMOIZE----------------------")
        print(f"---> {await result_fib(200)}")  # premier calcul → prend du temps
        print(f"---> {await result_fib(200)}")  # deuxième appel → instantané, car cache
        print(f"---> {await result_fib(250)}")  # calcule en réutilisant les résultats déjà en cache

    asyncio.run(main())
