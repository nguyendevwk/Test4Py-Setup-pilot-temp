import pytest
from flutes.iterator import drop_until

def test_drop_until_normal():
    """Elements before the first satisfying predicate are dropped."""
    data = [1, 2, 3, 4, 5, 6, 7]
    result = list(drop_until(lambda x: x > 4, data))
    assert result == [5, 6, 7], "Should drop elements until predicate is true"

def test_drop_until_no_match():
    """If no element satisfies the predicate, the iterator yields nothing."""
    data = [1, 2, 3]
    result = list(drop_until(lambda x: x > 10, data))
    assert result == [], "No element satisfies predicate, should return empty list"

def test_drop_until_invalid_iterable():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        list(drop_until(lambda x: x > 0, None))
