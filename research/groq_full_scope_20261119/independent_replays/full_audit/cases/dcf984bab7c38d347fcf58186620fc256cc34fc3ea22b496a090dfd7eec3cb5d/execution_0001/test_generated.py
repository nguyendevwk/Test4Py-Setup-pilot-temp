import itertools
import math
import pytest

from tqdm.contrib.itertools import combinations_with_replacement
from tqdm.auto import tqdm as tqdm_auto


def test_combinations_with_replacement_normal():
    """Verify correct combinations and total count for a normal case."""
    iterable = [1, 2, 3]
    r = 2
    # Disable progress bar output
    result = combinations_with_replacement(iterable, r, tqdm_class=tqdm_auto, disable=True)
    # Collect all combinations
    combos = list(result)
    expected = list(itertools.combinations_with_replacement(iterable, r))
    assert combos == expected, "Returned combinations do not match expected"
    # Total should be 6 for 3 items choose 2 with replacement
    assert result.total == 6, f"Expected total 6, got {result.total}"


def test_combinations_with_replacement_boundary_empty_iterable():
    """Test boundary case with empty iterable and r=0."""
    iterable = []
    r = 0
    result = combinations_with_replacement(iterable, r, tqdm_class=tqdm_auto, disable=True)
    combos = list(result)
    # combinations_with_replacement([], 0) yields one empty tuple
    assert combos == [()], "Expected a single empty tuple for r=0"
    # Total should be 1
    assert result.total == 1, f"Expected total 1, got {result.total}"


def test_combinations_with_replacement_error_non_iterable():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        # An integer is not iterable; itertools.combinations_with_replacement will raise
        combinations_with_replacement(5, 2, tqdm_class=tqdm_auto, disable=True)
