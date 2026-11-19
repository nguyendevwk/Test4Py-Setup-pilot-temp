import pytest
from py_backwards.utils.helpers import eager

# Test 1: Normal behavior – a generator that yields values
def test_eager_generates_list():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i

    result = gen_numbers()
    assert isinstance(result, list)
    assert result == [0, 1, 2]

# Test 2: Boundary case – an empty generator
def test_eager_empty_generator():
    @eager
    def empty_gen():
        if False:
            yield

    result = empty_gen()
    assert isinstance(result, list)
    assert result == []

# Test 3: Error propagation – the wrapped function raises an exception
def test_eager_propagates_exception():
    @eager
    def error_func():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        error_func()
