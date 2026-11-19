import pytest
from flutes.iterator import drop_until


def test_drop_until_basic():
    """Verify that elements are dropped until the predicate is satisfied."""
    result = list(drop_until(lambda x: x > 5, range(10)))
    assert result == [6, 7, 8, 9], "Expected to drop values <= 5 and keep the rest"


def test_drop_until_empty_iterable():
    """When the iterable is empty, the result should also be empty."""
    result = list(drop_until(lambda x: x > 0, []))
    assert result == [], "Dropping from an empty iterable should yield an empty list"


def test_drop_until_predicate_raises():
    """If the predicate raises an exception, it should propagate to the caller."""
    def bad_pred(x):
        if x == 3:
            raise ValueError("bad value")
        return True

    with pytest.raises(ValueError, match="bad value"):
        # The iterator will raise when it reaches the element 3
        list(drop_until(bad_pred, [1, 2, 3, 4]))
