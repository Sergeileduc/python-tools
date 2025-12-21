import time

import pytest

from python_tools_sl.decorators.pauses import with_pause, with_pause_async


def test_pause_decorator(monkeypatch):
    called = []

    @with_pause(seconds=0.1)
    def foo():
        called.append("ok")
        return 42

    start = time.perf_counter()
    result = foo()
    end = time.perf_counter()

    assert result == 42
    assert "ok" in called
    assert end - start >= 0.1  # vérifie qu'il y a bien eu pause


@pytest.mark.asyncio
async def test_with_pause_async_decorator():
    called = []

    @with_pause_async(seconds=0.1)
    async def foo_async():
        called.append("ok")
        return 99

    start = time.perf_counter()
    result = await foo_async()
    end = time.perf_counter()

    assert result == 99
    assert "ok" in called
    assert end - start >= 0.1  # vérifie qu'il y a bien eu pause
