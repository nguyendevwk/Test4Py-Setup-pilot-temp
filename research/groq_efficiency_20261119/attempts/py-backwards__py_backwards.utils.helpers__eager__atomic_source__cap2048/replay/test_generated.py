import pytest
from py_backwards.utils.helpers import eager

# Test 1: Normal behavior – generator yields multiple values
def test_eager_generates_list_of_values():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i * 10

    result = gen_numbers()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: Boundary case – generator yields no values
def test_eager_empty_generator_returns_empty_list():
    @eager
    def empty_gen():
        if False:
            yield 1

    result = empty_gen()
    assert result == []
    assert isinstance(result, list)

# Test 3: Error propagation – exception raised inside generator is not swallowed
def test_eager_propagates_exceptions():
    @eager
    def error_gen():
        yield 1
        raise ValueError("test error")
        yield 2

    with pytest.raises(ValueError, match="test error"):
        list(error_gen())
