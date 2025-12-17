import time
import functools


def timeit(func):
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction.
    Exemple:
        @timeit
        def slow_func():
            time.sleep(1)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMEIT] {func.__name__} exécutée en {end - start:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    Décorateur pour réessayer une fonction en cas d'exception.
    Args:
        max_attempts (int): nombre maximum de tentatives
        delay (int|float): délai entre tentatives en secondes
        exceptions (tuple): exceptions à intercepter
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(
                        f"[RETRY] {func.__name__} tentative {attempt} échouée: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator


def memoize(func):
    """
    Décorateur pour mettre en cache les résultats d'une fonction pure.
    Exemple:
        @memoize
        def fib(n):
            return n if n < 2 else fib(n-1) + fib(n-2)
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper
