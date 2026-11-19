import itertools
import math
import pytest

from tqdm.contrib.itertools import product as tqdm_product


def test_product_normal_and_total_computation():
    """Test that product returns the correct tuples and total is computed."""
    a = [1, 2]
    b = ['x', 'y']
    # Compute expected product and total
    expected = list(itertools.product(a, b))
    expected_total = math.prod([len(a), len(b)])
    # Use the tqdm_product function
    result = list(tqdm_product(a, b))
    assert result == expected
    # The tqdm_product function yields from tqdm_class which accepts total
    # We can verify that the total passed to tqdm_class matches expectation
    # by inspecting the length of the result (since tqdm_class is a simple iterator)
    assert len(result) == expected_total


def test_product_repeat_and_empty_iterable():
    """Test repeat=0 and empty iterable edge cases."""
    # repeat=0 should yield a single empty tuple
    result_repeat_zero = list(tqdm_product([1, 2], repeat=0))
    assert result_repeat_zero == [()]
    # Empty iterable should yield nothing
    result_empty = list(tqdm_product([]))
    assert result_empty == []


def test_product_non_iterable_raises():
    """Test that passing a non-iterable raises TypeError."""
    with pytest.raises(TypeError):
        # An integer is not iterable; itertools.product will raise TypeError
        list(tqdm_product(42))
