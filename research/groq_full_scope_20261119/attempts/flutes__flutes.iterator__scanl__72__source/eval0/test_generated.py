import pytest
from flutes.iterator import scanl

def test_scanl_basic_sum():
    """Normal behavior: summing a list with an initial value."""
    result = list(scanl(lambda a, b: a + b, [1, 2, 3, 4], 0))
    assert result == [0, 1, 3, 6, 10]

def test_scanl_empty_iterable_with_initial():
    """Boundary case: empty iterable but an initial value is provided."""
    result = list(scanl(lambda a, b: a + b, [], 42))
    assert result == [42]

def test_scanl_error_too_many_args():
    """Error case: passing more than one optional argument raises ValueError."""
    with pytest.raises(ValueError, match="Too many arguments"):
        list(scanl(lambda a, b: a + b, [1, 2], 0, 1))
