import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal behavior with a generator function
def test_eager_generates_list():
    @eager
    def gen_func():
        for i in range(3):
            yield i * 10

    result = gen_func()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: boundary case with an empty iterable
def test_eager_empty_iterable():
    @eager
    def empty_gen():
        if False:
            yield 1

    result = empty_gen()
    assert result == []
    assert isinstance(result, list)

# Test 3: error propagation when the wrapped function raises
def test_eager_propagates_exception():
    @eager
    def error_func():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        error_func()
