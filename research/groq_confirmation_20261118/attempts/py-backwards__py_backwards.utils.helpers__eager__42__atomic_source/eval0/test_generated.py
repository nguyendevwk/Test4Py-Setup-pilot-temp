import pytest
from py_backwards.utils.helpers import eager

# Test 1: Normal behavior – a generator that yields values
def test_eager_generates_list():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i * 10

    result = gen_numbers()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: Boundary case – generator that yields nothing
def test_eager_empty_generator():
    @eager
    def empty_gen():
        if False:
            yield 1

    result = empty_gen()
    assert isinstance(result, list)
    assert result == []

# Test 3: Error propagation – generator that raises an exception
def test_eager_propagates_exception():
    @eager
    def error_gen():
        yield 1
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        list(error_gen())
