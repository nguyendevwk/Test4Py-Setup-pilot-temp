import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal behavior – a generator function should be converted to a list
def test_eager_converts_generator_to_list():
    @eager
    def gen_func():
        for i in range(3):
            yield i * 10

    result = gen_func()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: boundary case – an empty iterable should produce an empty list
def test_eager_handles_empty_iterable():
    @eager
    def empty_gen():
        if False:
            yield

    result = empty_gen()
    assert result == []
    assert isinstance(result, list)

# Test 3: error propagation – exceptions raised inside the wrapped function should not be swallowed
def test_eager_propagates_exceptions():
    @eager
    def error_func():
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        error_func()
