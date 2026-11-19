import pytest
from flutes.iterator import drop_until

def test_drop_until_basic():
    """Normal case: drop elements until predicate satisfied."""
    result = list(drop_until(lambda x: x > 5, range(10)))
    assert result == [6, 7, 8, 9], "Should drop 0-5 and return the rest"

def test_drop_until_boundary():
    """Boundary cases: predicate never true and true at first element."""
    # Predicate never true: should return empty iterator
    empty = list(drop_until(lambda x: x > 10, range(5)))
    assert empty == [], "No element satisfies predicate, result should be empty"

    # Predicate true at first element: should return full iterator
    full = list(drop_until(lambda x: x == 0, range(5)))
    assert full == [0, 1, 2, 3, 4], "First element satisfies predicate, all elements should be returned"

def test_drop_until_error():
    """Error case: passing a non-iterable should raise TypeError."""
    with pytest.raises(TypeError):
        # The function expects an iterable; passing an int should fail
        list(drop_until(lambda x: x > 0, 42))
