# `python_tools_sl.decorators`

Suite de décorateurs **synchrones** et **asynchrones** conçus pour améliorer la lisibilité, la robustesse et l’ergonomie du code Python.  
Les décorateurs sont strictement typés (`P`, `R`, `Decorator`, `AsyncDecorator`) et suivent une grammaire cohérente entre versions sync et async.

---

## ✨ Fonctionnalités

- Décorateurs **sync** et **async** parfaitement symétriques  
- Typage strict compatible mypy / Pylance  
- API claire et stable  
- Cas d’usage courants :  
  - mesure de performance  
  - retry automatique  
  - pause contrôlée  
  - mémoïsation  
- Code lisible, minimaliste et maintenable

---

## 📦 Import

```python
from python_tools_sl.decorators import (
    # Sync
    with_pause,
    timeit,
    retry,
    memoize,

    # Async
    with_pause_async,
    timeit_async,
    retry_async,
    memoize_async,
)
```

---

## 🧩 Décorateurs synchrones

### `with_pause(seconds=2, message=None)`

Ajoute une pause après l’exécution d’une fonction.

```python
@with_pause(seconds=1.5)
def fetch():
    return http_get()
```

---

### `timeit(prefix="[TIMEIT]")`

Mesure le temps d’exécution d’une fonction.

```python
@timeit()
def compute():
    heavy_work()
```

---

### `retry(max_attempts=3, delay=1.0, exceptions=(Exception,))`

Réessaie une fonction en cas d’exception.

```python
@retry(max_attempts=5, delay=0.5, exceptions=(ValueError,))
def fragile():
    return sometimes_fails()
```

---

### `memoize`

Met en cache les résultats d’une fonction pure.

```python
@memoize
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

---

## 🌙 Décorateurs asynchrones

### `with_pause_async(seconds=2, message=None)`

Ajoute une pause après une coroutine.

```python
@with_pause_async(seconds=1)
async def fetch():
    return await http_get()
```

---

### `timeit_async(prefix="[ASYNC TIMEIT]")`

Mesure le temps d’exécution d’une coroutine.

```python
@timeit_async()
async def compute():
    await asyncio.sleep(1)
```

---

### `retry_async(max_attempts=3, delay=1.0, exceptions=(Exception,))`

Réessaie une coroutine en cas d’exception.

```python
@retry_async(max_attempts=3, delay=0.5)
async def fragile():
    return await sometimes_fails()
```

---

### `memoize_async`

Met en cache les résultats d’une coroutine.

```python
@memoize_async
async def fib(n):
    return n if n < 2 else await fib(n-1) + await fib(n-2)
```

---

## 🧠 Typage

Les décorateurs reposent sur des helpers typés :

```python
P = ParamSpec("P")
R = TypeVar("R")

Decorator = Callable[[Callable[P, R]], Callable[P, R]]
AsyncDecorator = Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]
```

Cette grammaire garantit :

- une signature préservée  
- un typage strict  
- une symétrie parfaite sync/async  

---

## 📁 Structure du module

```bash
decorators/
│
├── sync.py          # Décorateurs synchrones
├── async_.py        # Décorateurs asynchrones
└── __init__.py      # API publique
```

---

## 🧭 Philosophie

- **Explicite > implicite**  
- **Simplicité > magie**  
- **Typage strict** pour éviter les erreurs silencieuses  
- **Symétrie sync/async** pour une API prévisible  
- **Documentation claire** pour une maintenance sereine  
