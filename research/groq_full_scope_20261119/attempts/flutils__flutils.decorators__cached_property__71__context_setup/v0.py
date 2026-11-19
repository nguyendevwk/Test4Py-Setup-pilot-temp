import asyncio
import types
import pytest
from flutils.decorators import cached_property


def test_cached_property_evaluates_once_and_caches():
    class Counter:
        def __init__(self):
            self.calls = 0

        @cached_property
        def value(self):
            self.calls += 1
            return 42

    obj = Counter()
    # First access computes value
    assert obj.value == 42
    assert obj.calls == 1
    # Subsequent accesses use cached value
    assert obj.value == 42
    assert obj.calls == 1
    # Deleting the attribute resets the property
    del obj.value
    assert obj.calls == 1
    # Access again recomputes
    assert obj.value == 42
    assert obj.calls == 2


def test_cached_property_on_coroutine_function():
    class AsyncHolder:
        @cached_property
        async def async_value(self):
            await asyncio.sleep(0.01)
            return "done"

    async def run_test():
        holder = AsyncHolder()
        # First access returns a coroutine that schedules the task
        coro = holder.async_value
        assert isinstance(coro, types.CoroutineType)
        # Await the coroutine to get the result
        result = await coro
        assert result == "done"
        # After awaiting, the attribute is replaced with the Future object
        future = holder.async_value
        assert isinstance(future, asyncio.Future)
        assert future.done()
        assert future.result() == "done"

    asyncio.run(run_test())


def test_cached_property_on_non_coroutine_and_coroutine_mix():
    class Mixed:
        def __init__(self):
            self.counter = 0

        @cached_property
        def sync_prop(self):
            self.counter += 1
            return self.counter

        @cached_property
        async def async_prop(self):
            await asyncio.sleep(0.01)
            return self.counter * 10

    async def run_mix():
        m = Mixed()
        # Sync property
        assert m.sync_prop == 1
        assert m.sync_prop == 1  # cached
        # Async property
        async_coro = m.async_prop
        assert isinstance(async_coro, types.CoroutineType)
        async_result = await async_coro
        assert async_result == 10
        # After awaiting, async_prop is a Future
        future = m.async_prop
        assert isinstance(future, asyncio.Future)
        assert future.done()
        assert future.result() == 10

    asyncio.run(run_mix())
