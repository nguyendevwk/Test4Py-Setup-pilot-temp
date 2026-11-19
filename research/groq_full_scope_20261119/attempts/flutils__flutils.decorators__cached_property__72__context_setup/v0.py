import asyncio
import pytest
from flutils.decorators import cached_property


def test_cached_property_evaluates_once_and_is_stored():
    class Counter:
        def __init__(self):
            self.calls = 0

        @cached_property
        def value(self):
            self.calls += 1
            return 42

    obj = Counter()
    # First access computes and stores the value
    assert obj.value == 42
    assert obj.calls == 1
    # Subsequent access returns stored value without recomputing
    assert obj.value == 42
    assert obj.calls == 1
    # The value is stored directly in the instance dict
    assert "value" in obj.__dict__
    assert obj.__dict__["value"] == 42


def test_cached_property_can_be_reset_by_deletion():
    class Counter:
        def __init__(self):
            self.calls = 0

        @cached_property
        def value(self):
            self.calls += 1
            return self.calls

    obj = Counter()
    assert obj.value == 1
    assert obj.calls == 1
    # Delete the cached attribute
    del obj.value
    # Next access recomputes the value
    assert obj.value == 2
    assert obj.calls == 2
    # Deleting again resets again
    del obj.value
    assert obj.value == 3
    assert obj.calls == 3


@pytest.mark.asyncio
async def test_cached_property_supports_coroutine_functions():
    class AsyncCounter:
        def __init__(self):
            self.calls = 0

        @cached_property
        async def value(self):
            self.calls += 1
            await asyncio.sleep(0.01)
            return self.calls

    obj = AsyncCounter()
    # First access returns a coroutine that resolves to the value
    result = await obj.value
    assert result == 1
    assert obj.calls == 1
    # Subsequent access returns the same future object stored in __dict__
    future1 = obj.__dict__["value"]
    future2 = await obj.value
    assert future1 is obj.__dict__["value"]
    assert future2 == 1
    # The future is already resolved
    assert future1.done()
    assert future1.result() == 1
