import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal behavior – a generator function returns a list of values
def test_eager_with_generator():
    @eager
    def gen_func():
        for i in range(3):
            yield i * 10

    result = gen_func()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: boundary case – an empty iterable is converted to an empty list
def test_eager_with_empty_iterable():
    @eager
    def empty_func():
        return iter([])

    result = empty_func()
    assert result == []

# Test 3: error propagation – exceptions raised inside the wrapped function are not swallowed
def test_eager_propagates_exceptions():
    @eager
    def error_func():
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        error_func()
