import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal behavior – a generator function returns a list of values
def test_eager_with_generator():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i * 10

    result = gen_numbers()
    assert isinstance(result, list)
    assert result == [0, 10, 20]

# Test 2: boundary case – the wrapped function yields nothing
def test_eager_with_empty_iterable():
    @eager
    def empty_gen():
        if False:
            yield 1

    result = empty_gen()
    assert result == []

# Test 3: error propagation – exceptions raised inside the original function are not swallowed
def test_eager_propagates_exceptions():
    @eager
    def faulty():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        faulty()
