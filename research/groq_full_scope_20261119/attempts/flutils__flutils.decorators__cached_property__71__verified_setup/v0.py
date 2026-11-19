import asyncio
import types
import pytest
from flutils.decorators import cached_property


class Simple:
    def __init__(self):
        self.counter = 0

    @cached_property
    def value(self):
        self.counter += 1
        return self.counter


class AsyncExample:
    def __init__(self):
        self.calls = 0

    @cached_property
    async def async_value(self):
        self.calls += 1
        await asyncio.sleep(0.01)
        return self.calls


def test_cached_property_evaluates_once_and_can_be_reset():
    obj = Simple()
    # First access computes the value and increments counter
    assert obj.value == 1
    assert obj.counter == 1
    # Subsequent access returns cached value without recomputation
    assert obj.value == 1
    assert obj.counter == 1
    # Deleting the attribute forces recomputation
    del obj.value
    assert obj.value == 2
    assert obj.counter == 2


@pytest.mark.asyncio
async def test_cached_property_with_coroutine():
    obj = AsyncExample()
    # First await triggers coroutine execution and caching
    result = await obj.async_value
    assert result == 1
    assert obj.calls == 1
    # Subsequent await returns cached future result
    result2 = await obj.async_value
    assert result2 == 1
    assert obj.calls == 1
    # Deleting the attribute resets the cached future
    del obj.async_value
    result3 = await obj.async_value
    assert result3 == 2
    assert obj.calls == 2


def test_cached_property_is_descriptor_on_class():
    # The descriptor should be accessible via the class
    assert isinstance(Simple.value, cached_property)
    # Accessing via the class returns the descriptor itself
    assert Simple.value is Simple.__dict__['value']
    # Accessing via an instance returns the cached value
    instance = Simple()
    assert instance.value == 1
    # The descriptor is not stored in the instance dict after first access
    assert 'value' not in instance.__dict__
