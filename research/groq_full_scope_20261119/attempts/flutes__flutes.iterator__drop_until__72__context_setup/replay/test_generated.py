import pytest
from flutes.iterator import drop_until


def test_drop_until_basic():
    """Normal case: drop elements until predicate is true."""
    result = list(drop_until(lambda x: x > 5, range(10)))
    assert result == [6, 7, 8, 9], "Should drop 0-5 and return the rest"


def test_drop_until_no_match():
    """Boundary case: predicate never matches; should return empty iterator."""
    result = list(drop_until(lambda x: x > 10, range(5)))
    assert result == [], "No element satisfies predicate, so result is empty"


def test_drop_until_invalid_iterable():
    """Error case: non-iterable input should raise TypeError."""
    with pytest.raises(TypeError):
        list(drop_until(lambda x: True, 42))
