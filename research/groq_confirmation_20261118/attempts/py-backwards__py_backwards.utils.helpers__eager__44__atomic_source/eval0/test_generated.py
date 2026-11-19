import pytest
from py_backwards.utils.helpers import eager

# Test 1: Normal generator returns list of values
def test_eager_with_generator():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i
    result = gen_numbers()
    assert result == [0, 1, 2]
    assert isinstance(result, list)

# Test 2: Empty generator returns empty list
def test_eager_with_empty_generator():
    @eager
    def empty_gen():
        if False:
            yield
    result = empty_gen()
    assert result == []
    assert isinstance(result, list)

# Test 3: Function that raises an exception propagates the error
def test_eager_propagates_exception():
    @eager
    def error_gen():
        raise ValueError("test error")
    with pytest.raises(ValueError, match="test error"):
        error_gen()
