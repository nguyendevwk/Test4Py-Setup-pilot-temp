import pytest
from flutes.iterator import drop_until


def test_drop_until_basic():
    """Normal case: drop elements until predicate is true."""
    result = list(drop_until(lambda x: x > 5, range(10)))
    assert result == [6, 7, 8, 9]


def test_drop_until_no_match():
    """Boundary case: predicate never matches, all elements are dropped."""
    result = list(drop_until(lambda x: x > 10, range(5)))
    assert result == []


def test_drop_until_invalid_iterable():
    """Error case: non‑iterable passed to drop_until raises TypeError."""
    with pytest.raises(TypeError):
        list(drop_until(lambda x: True, 42))
