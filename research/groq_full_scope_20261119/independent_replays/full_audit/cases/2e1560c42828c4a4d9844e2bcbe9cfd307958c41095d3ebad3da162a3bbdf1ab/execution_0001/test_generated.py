import pytest
from tqdm.auto import trange

def test_trange_basic_sequence(tmp_path):
    # Verify that trange yields the correct sequence and accepts a description
    seq = list(trange(5, desc="counting", leave=False))
    assert seq == [0, 1, 2, 3, 4]
    # The description should be set on the underlying tqdm instance
    # We can check that the description attribute is present and correct
    # by inspecting the first element's tqdm object (it is a generator)
    # Since tqdm returns an iterator, we cannot directly access the tqdm object here,
    # but we can ensure that no exception was raised during iteration.

def test_trange_zero_length(tmp_path):
    # trange with zero length should produce an empty iterator
    seq = list(trange(0))
    assert seq == []

def test_trange_invalid_input():
    # Passing a non-integer to trange should raise a TypeError from range
    with pytest.raises(TypeError):
        list(trange(3.5))
