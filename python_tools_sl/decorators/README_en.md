# `python_tools_sl.decorators`

A collection of **synchronous** and **asynchronous** decorators designed to improve clarity, robustness, and ergonomics in Python code.  
All decorators are strictly typed (`P`, `R`, `Decorator`, `AsyncDecorator`) and follow a consistent grammar between sync and async variants.

---

## ✨ Features

- Perfectly symmetrical **sync** and **async** decorators  
- Strict typing compatible with mypy / Pylance  
- Clear and stable public API  
- Covers common use cases:
  - performance measurement  
  - automatic retries  
  - controlled pauses  
  - memoization  
- Clean, minimalistic, maintainable code

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

## 🧩 Synchronous decorators

### `with_pause(seconds=2, message=None)`

Adds a pause after the execution of a function.

```python
@with_pause(seconds=1.5)
def fetch():
    return http_get()
```

---

### `timeit(prefix="[TIMEIT]")`

Measures the execution time of a function.

```python
@timeit()
def compute():
    heavy_work()
```

---

### `retry(max_attempts=3, delay=1.0, exceptions=(Exception,))`

Retries a function when an exception occurs.

```python
@retry(max_attempts=5, delay=0.5, exceptions=(ValueError,))
def fragile():
    return sometimes_fails()
```

---

### `memoize`

Caches the results of a pure function.

```python
@memoize
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

---

## 🌙 Asynchronous decorators

### `with_pause_async(seconds=2, message=None)`

Adds a pause after an async function.

```python
@with_pause_async(seconds=1)
async def fetch():
    return await http_get()
```

---

### `timeit_async(prefix="[ASYNC TIMEIT]")`

Measures the execution time of an async function.

```python
@timeit_async()
async def compute():
    await asyncio.sleep(1)
```

---

### `retry_async(max_attempts=3, delay=1.0, exceptions=(Exception,))`

Retries an async function when an exception occurs.

```python
@retry_async(max_attempts=3, delay=0.5)
async def fragile():
    return await sometimes_fails()
```

---

### `memoize_async`

Caches the results of an async function.

```python
@memoize_async
async def fib(n):
    return n if n < 2 else await fib(n-1) + await fib(n-2)
```

---

## 🧠 Typing

The decorators rely on typed helper aliases:

```python
P = ParamSpec("P")
R = TypeVar("R")

Decorator = Callable[[Callable[P, R]], Callable[P, R]]
AsyncDecorator = Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]
```

This grammar ensures:

- preserved function signatures  
- strict typing  
- perfect sync/async symmetry  

---

## 📁 Module structure

```bash
decorators/
│
├── sync.py          # Synchronous decorators
├── async_.py        # Asynchronous decorators
└── __init__.py      # Public API
```

---

## 🧭 Philosophy

- **Explicit > implicit**  
- **Simplicity > magic**  
- **Strict typing** to avoid silent errors  
- **Sync/async symmetry** for predictable APIs  
- **Clear documentation** for long-term maintainability  
