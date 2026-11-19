import asyncio
import types
import pytest
from flutils.decorators import cached_property


class Simple:
    def __init__(self, value):
        self.value = value

    @cached_property
    def computed(self):
        """Return the stored value plus one."""
        return self.value + 1


class AsyncSimple:
    def __init__(self, value):
        self.value = value

    @cached_property
    async def async_computed(self):
        """Return the stored value multiplied by two asynchronously."""
        await asyncio.sleep(0)  # simulate async work
        return self.value * 2


def test_cached_property_evaluates_once_and_caches(tmp_path):
    """The property should compute once and then return the cached value."""
    obj = Simple(10)
    # First access triggers computation
    first = obj.computed
    assert first == 11
    # The value is stored in the instance dict
    assert "computed" in obj.__dict__
    # Subsequent access returns the cached value without recomputation
    second = obj.computed
    assert second == 11
    # Mutating the underlying attribute should not affect the cached value
    obj.value = 20
    assert obj.computed == 11


def test_cached_property_deletion_resets_computation(tmp_path):
    """Deleting the cached attribute should force recomputation on next access."""
    obj = Simple(5)
    assert obj.computed == 6
    # Delete the cached value
    del obj.computed
    # The attribute is no longer in the instance dict
    assert "computed" not in obj.__dict__
    # Next access recomputes
    assert obj.computed == 6
    # Changing the underlying value should affect the recomputed result
    obj.value = 7
    del obj.computed
    assert obj.computed == 8


@pytest.mark.asyncio
async def test_cached_property_with_coroutine(tmp_path):
    """A coroutine property should be wrapped and cached as a Future."""
    obj = AsyncSimple(3)
    # First access returns a coroutine object
    coro = obj.async_computed
    assert isinstance(coro, types.CoroutineType)
    # Awaiting the coroutine yields the correct result
    result = await coro
    assert result == 6
    # The coroutine result is cached as a Future in the instance dict
    cached = obj.__dict__["async_computed"]
    assert isinstance(cached, asyncio.Future)
    # Awaiting the cached future returns the same result
    assert await cached == 6
    # Subsequent access returns the same Future object
    assert obj.async_computed is cached
