import pytest
from tqdm.auto import trange

def test_trange_normal_iteration():
    """trange should iterate over the given range and return the same values."""
    result = list(trange(5, desc="test"))
    assert result == [0, 1, 2, 3, 4]
    # The returned object should be an instance of tqdm.auto.tqdm
    from tqdm.auto import tqdm
    assert isinstance(trange(3), tqdm)

def test_trange_zero_and_negative():
    """trange with zero or negative bounds should produce an empty iterator."""
    assert list(trange(0)) == []
    assert list(trange(-3)) == []

def test_trange_invalid_argument():
    """trange should raise a TypeError when the range argument is not an integer."""
    with pytest.raises(TypeError):
        list(trange(1.5))
