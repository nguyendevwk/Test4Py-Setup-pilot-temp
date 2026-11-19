import pytest
from flutes.iterator import scanl


def test_scanl_with_initial_value():
    """Normal case: provide an explicit initial accumulator."""
    result = list(scanl(lambda acc, x: acc + x, [1, 2, 3], 0))
    assert result == [0, 1, 3, 6], "scanl should accumulate correctly with initial value"


def test_scanl_empty_iterable_uses_first_element():
    """Boundary case: empty iterable should raise StopIteration when no initial is given."""
    with pytest.raises(StopIteration):
        # The function will attempt to call next() on an empty iterator
        list(scanl(lambda acc, x: acc + x, []))


def test_scanl_too_many_arguments_raises_value_error():
    """Error case: providing more than one extra argument should raise ValueError."""
    with pytest.raises(ValueError, match="Too many arguments"):
        list(scanl(lambda acc, x: acc + x, [1, 2, 3], 0, 1))
