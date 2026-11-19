import asyncio
import types
import pytest
from flutils.decorators import cached_property


class Simple:
    def __init__(self, value):
        self.value = value

    @cached_property
    def double(self):
        """Return double of value."""
        return self.value * 2


class AsyncHolder:
    def __init__(self, value):
        self.value = value

    @cached_property
    async def async_double(self):
        await asyncio.sleep(0.01)
        return self.value * 2


def test_cached_property_evaluates_once_and_caches(tmp_path):
    obj = Simple(10)
    # First access triggers computation
    first = obj.double
    assert first == 20
    # Subsequent access retrieves cached value directly from __dict__
    second = obj.double
    assert second == 20
    # Ensure the value is stored in the instance dictionary
    assert "double" in obj.__dict__
    assert obj.__dict__["double"] == 20


def test_cached_property_deletion_resets_computation(tmp_path):
    obj = Simple(5)
    assert obj.double == 10
    # Delete the cached attribute
    del obj.double
    # After deletion, accessing again recomputes
    recomputed = obj.double
    assert recomputed == 10
    # Ensure the attribute is again present in __dict__
    assert "double" in obj.__dict__


@pytest.mark.asyncio
async def test_cached_property_async_behavior(tmp_path):
    obj = AsyncHolder(7)
    # First access returns a coroutine that resolves to the value
    coro = obj.async_double
    assert isinstance(coro, types.CoroutineType)
    result = await coro
    assert result == 14
    # After awaiting, the value is cached as a Future in __dict__
    cached = obj.__dict__["async_double"]
    assert isinstance(cached, asyncio.Future)
    assert cached.done()
    assert cached.result() == 14
    # Subsequent access returns the same Future object
    same_future = obj.async_double
    assert same_future is cached
