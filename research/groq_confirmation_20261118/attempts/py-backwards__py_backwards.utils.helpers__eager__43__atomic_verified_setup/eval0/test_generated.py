import pytest
from py_backwards.utils.helpers import eager

# Test 1: normal behavior – generator yields values
def test_eager_generates_list():
    @eager
    def gen_numbers():
        for i in range(3):
            yield i
    result = gen_numbers()
    assert result == [0, 1, 2]
    assert isinstance(result, list)

# Test 2: boundary case – empty generator
def test_eager_empty_generator():
    @eager
    def empty_gen():
        if False:
            yield
    result = empty_gen()
    assert result == []
    assert isinstance(result, list)

# Test 3: error propagation – function raises exception
def test_eager_propagates_exception():
    @eager
    def faulty():
        raise ValueError("boom")
    with pytest.raises(ValueError, match="boom"):
        faulty()
