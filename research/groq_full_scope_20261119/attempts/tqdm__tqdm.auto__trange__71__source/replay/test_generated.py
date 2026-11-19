import pytest
from tqdm.auto import trange

def test_trange_basic_sequence():
    """trange should iterate over the same values as range."""
    result = list(trange(5))
    assert result == [0, 1, 2, 3, 4], "trange should yield the same sequence as range(5)"

def test_trange_with_desc_and_total():
    """trange should accept tqdm kwargs such as desc and total."""
    # Using a small range to keep the test fast
    iterator = trange(3, desc="test", total=3)
    # The iterator should still produce the correct values
    assert list(iterator) == [0, 1, 2], "trange should yield the correct values even with kwargs"
    # The iterator should expose the desc attribute set by tqdm
    assert getattr(iterator, "desc", None) == "test", "trange should set the desc attribute on the iterator"

def test_trange_invalid_input_raises():
    """trange should raise a TypeError when given a non-integer argument to range."""
    with pytest.raises(TypeError):
        list(trange("invalid"))
