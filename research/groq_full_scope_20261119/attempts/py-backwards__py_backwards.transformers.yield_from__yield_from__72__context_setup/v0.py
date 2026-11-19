import pytest
from py_backwards.transformers.yield_from import yield_from

def test_yield_from_normal_iteration():
    # A simple generator that yields three values
    def gen():
        for i in range(3):
            yield i
    # Collect the yielded values
    result = list(yield_from(gen(), None, None))
    assert result == [0, 1, 2], "yield_from should yield all items from the generator"

def test_yield_from_empty_generator():
    # An empty generator should produce no values
    def empty_gen():
        if False:
            yield
    result = list(yield_from(empty_gen(), None, None))
    assert result == [], "yield_from should yield nothing for an empty generator"

def test_yield_from_non_iterable_raises():
    # Passing a non-iterable should raise a TypeError when iter() is called
    with pytest.raises(TypeError):
        list(yield_from(42, None, None))
