import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal generator returns list of values
def test_eager_with_generator():
    @eager
    def gen_func(x: int):
        for i in range(x):
            yield i * 2

    result = gen_func(3)
    assert isinstance(result, list)
    assert result == [0, 2, 4]

# Test 2: boundary case – empty iterable
def test_eager_with_empty_iterable():
    @eager
    def empty_func():
        return iter([])

    result = empty_func()
    assert result == []
    assert isinstance(result, list)

# Test 3: error propagation – function raises exception
def test_eager_propagates_exception():
    @eager
    def error_func():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        error_func()
