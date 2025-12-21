import time
from functools import wraps
from typing import Any, Callable, Dict, ParamSpec, Tuple, Type, TypeVar

from python_tools_sl.utils.formatting import format_duration

P = ParamSpec("P")  # capture la signature des paramètres
R = TypeVar("R")  # capture le type de retour


def timeit(prefix: str = "[TIMEIT]"):
    """
    Décorateur paramétrable qui mesure et affiche le temps d'exécution d'une fonction.

    Args:
        prefix (str, optionnel): Texte affiché avant le nom de la fonction dans le log.
            Par défaut "[TIMEIT]".

    Returns:
        Callable: Un décorateur qui peut être appliqué à une fonction pour chronométrer son exécution.

    Exemple:
        @timeit()
        def foo():
            time.sleep(0.1)

        @timeit(prefix="[BENCH]")
        def bar():
            time.sleep(0.2)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"{prefix} {func.__name__} exécutée en {format_duration(end - start)}")
            return result

        return wrapper

    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """
    Décorateur qui réessaie l'exécution d'une fonction en cas d'exception.

    Args:
        max_attempts (int): Nombre maximum de tentatives (par défaut 3).
        delay (float): Délai en secondes entre deux tentatives (par défaut 1.0).
        exceptions (Tuple[Type[Exception], ...]): Types d'exceptions qui déclenchent
            un nouvel essai. Par défaut, toutes les exceptions (`Exception`).

    Returns:
        Callable[P, R]: La fonction décorée, avec la même signature et type de retour.

    Exemple:
        @retry(max_attempts=5, delay=0.5, exceptions=(ValueError,))
        def fragile_func(x: int) -> int:
            if x < 0:
                raise ValueError("x doit être positif")
            return x * 2
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"⚠️ Tentative {attempt}/{max_attempts} échouée : {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            if last_exc is not None:
                raise last_exc
            raise RuntimeError("Échec du retry: aucune exception capturée")

        return wrapper

    return decorator


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """
    Décorateur pour mettre en cache les résultats d'une fonction pure.

    Le cache est basé sur les arguments passés à la fonction.
    Attention : les arguments doivent être hashables (ex. int, str, tuple).

    Exemple:
        @memoize
        def fib(n: int) -> int:
            return n if n < 2 else fib(n-1) + fib(n-2)
    """
    cache: Dict[tuple[Any, ...], R] = {}

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # clé basée sur args + kwargs (triés pour être hashables)
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


if __name__ == "__main__":
    # RETRY
    @retry(max_attempts=3, delay=0.5, exceptions=(ZeroDivisionError,))
    def fragile_division(a: int, b: int) -> float:
        """Division qui peut échouer si b == 0"""
        return a / b

    try:
        print(fragile_division(10, 2))  # -> 5.0
        print(fragile_division(10, 0))  # -> relance ZeroDivisionError après 3 tentatives
    except ZeroDivisionError:
        print("ok, Zero Division Error Impossible. Nombre d'essai max atteing")

    # TIMEIT
    @timeit()
    def long(a: int, b: int) -> int:
        r = a + b
        time.sleep(1)
        return r

    print(long(1, 3))

    # MEMOIZE
    @memoize
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    @timeit(prefix="[BENCH]")
    def result_fib(n: int) -> int:
        return fib(n)

    print(f"---> {result_fib(200)}")  # premier calcul → prend du temps
    print(f"---> {result_fib(200)}")  # deuxième appel → instantané, car cache
    print(f"---> {result_fib(250)}")  # calcule en réutilisant les résultats déjà en cache
