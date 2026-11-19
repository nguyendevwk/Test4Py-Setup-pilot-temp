import pytest
from httpie.utils import split_iterable

def test_split_iterable_basic():
    """Verify that items are correctly partitioned based on a simple predicate."""
    data = [1, 2, 3, 4, 5]
    # predicate: even numbers
    left, right = split_iterable(data, lambda x: x % 2 == 0)
    assert left == [2, 4], f"Expected evens in left, got {left}"
    assert right == [1, 3, 5], f"Expected odds in right, got {right}"

def test_split_iterable_all_true_and_all_false():
    """Check behavior when all items satisfy or do not satisfy the predicate."""
    data = ['a', 'b', 'c']
    # all true
    left, right = split_iterable(data, lambda x: True)
    assert left == data, f"All items should be in left, got {left}"
    assert right == [], f"Right should be empty, got {right}"
    # all false
    left, right = split_iterable(data, lambda x: False)
    assert left == [], f"Left should be empty, got {left}"
    assert right == data, f"All items should be in right, got {right}"

def test_split_iterable_empty_iterable():
    """Ensure that an empty iterable returns two empty lists without error."""
    empty = []
    left, right = split_iterable(empty, lambda x: True)
    assert left == [], "Left should be empty for empty input"
    assert right == [], "Right should be empty for empty input"
