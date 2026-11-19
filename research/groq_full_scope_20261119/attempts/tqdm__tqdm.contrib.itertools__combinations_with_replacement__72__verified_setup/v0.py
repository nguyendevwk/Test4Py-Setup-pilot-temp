import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_normal():
    # Normal case: list of 3 elements, r=2
    iterable = ['a', 'b', 'c']
    r = 2
    result = list(combinations_with_replacement(iterable, r))
    # Expected combinations
    expected = [
        ('a', 'a'), ('a', 'b'), ('a', 'c'),
        ('b', 'b'), ('b', 'c'),
        ('c', 'c')
    ]
    assert result == expected
    # The tqdm wrapper should have the correct total
    # For n=3, r=2: total = C(3+2-1, 2) = C(4,2) = 6
    assert result.__iter__().__self__.total == 6

def test_combinations_with_replacement_empty_and_zero():
    # Edge case: empty iterable with r=0 should yield one empty tuple
    iterable = []
    r = 0
    result = list(combinations_with_replacement(iterable, r))
    assert result == [()]
    # Total should be 1
    assert result.__iter__().__self__.total == 1

def test_combinations_with_replacement_invalid_iterable():
    # Passing a non-iterable should raise a TypeError from itertools
    with pytest.raises(TypeError):
        list(combinations_with_replacement(42, 2))
