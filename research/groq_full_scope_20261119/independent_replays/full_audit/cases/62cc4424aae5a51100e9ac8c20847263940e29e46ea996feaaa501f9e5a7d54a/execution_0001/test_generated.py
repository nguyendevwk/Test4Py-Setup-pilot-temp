import pytest
from flutes.iterator import drop_until

def test_drop_until_normal_behavior():
    """When the predicate becomes true, all subsequent items are yielded."""
    data = [1, 2, 3, 4, 5, 6, 7]
    result = list(drop_until(lambda x: x > 4, data))
    assert result == [5, 6, 7], "Should drop items until predicate is true and then yield the rest"

def test_drop_until_boundary_conditions():
    """Edge cases: empty iterable and predicate never satisfied."""
    # Empty iterable
    empty = []
    assert list(drop_until(lambda x: x > 0, empty)) == [], "Empty input should yield empty output"

    # Predicate never satisfied
    data = [1, 2, 3]
    assert list(drop_until(lambda x: x > 10, data)) == [], "No element satisfies predicate, should return empty"

    # Predicate true at first element
    data = [10, 20, 30]
    assert list(drop_until(lambda x: x > 5, data)) == [10, 20, 30], "First element satisfies predicate, all should be yielded"

def test_drop_until_error_behavior():
    """Passing a non-callable predicate should raise a TypeError."""
    data = [1, 2, 3]
    with pytest.raises(TypeError):
        list(drop_until(42, data))  # 42 is not callable
