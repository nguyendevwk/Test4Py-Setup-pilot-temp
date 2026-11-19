import itertools
import pytest
from tqdm.contrib.itertools import chain

def test_chain_with_lists_total_auto():
    """When iterables are sequences, total is inferred automatically."""
    seq1 = [1, 2, 3]
    seq2 = [4, 5]
    # Use chain to iterate over both sequences
    result = list(chain(seq1, seq2))
    assert result == [1, 2, 3, 4, 5]
    # The returned tqdm object should have the correct total
    # We can access the internal iterator to get the tqdm instance
    # Since chain returns tqdm, we can inspect its total attribute
    # by creating the tqdm instance directly
    tqdm_obj = chain(seq1, seq2)
    assert tqdm_obj.total == len(seq1) + len(seq2)

def test_chain_with_generators_no_total():
    """When iterables are generators, total is not inferred and remains None."""
    gen1 = (x for x in range(3))
    gen2 = (x for x in range(2, 5))
    # Iterate and collect results
    result = list(chain(gen1, gen2))
    assert result == [0, 1, 2, 2, 3, 4]
    # The tqdm object should have total=None because generators have no len
    tqdm_obj = chain(gen1, gen2)
    assert tqdm_obj.total is None

def test_chain_non_iterable_error():
    """Passing a non-iterable to chain should raise a TypeError."""
    non_iter = 42  # int is not iterable
    with pytest.raises(TypeError):
        list(chain(non_iter))
