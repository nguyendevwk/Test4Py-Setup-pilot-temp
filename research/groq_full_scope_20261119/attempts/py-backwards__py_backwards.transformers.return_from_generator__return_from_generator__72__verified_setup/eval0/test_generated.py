import pytest
from py_backwards.transformers.return_from_generator import return_from_generator

def test_return_from_generator_with_integer():
    """Return value should be an integer and accessible via StopIteration.value."""
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator(42)
    assert excinfo.value.value == 42, "StopIteration.value should be the integer 42"

def test_return_from_generator_with_list():
    """Return value should be a list and accessible via StopIteration.value."""
    sample_list = [1, 2, 3]
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator(sample_list)
    assert excinfo.value.value == sample_list, "StopIteration.value should be the list [1, 2, 3]"

def test_return_from_generator_with_none():
    """Return value should be None and accessible via StopIteration.value."""
    with pytest.raises(StopIteration) as excinfo:
        return_from_generator(None)
    assert excinfo.value.value is None, "StopIteration.value should be None"
