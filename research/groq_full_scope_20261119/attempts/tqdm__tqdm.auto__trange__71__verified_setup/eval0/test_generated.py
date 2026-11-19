import pytest
from tqdm.auto import trange

def test_trange_basic_sequence(tmp_path):
    # trange should iterate over the same values as range
    seq = list(trange(5))
    assert seq == [0, 1, 2, 3, 4], "trange should yield the same sequence as range"

def test_trange_with_desc_and_total(tmp_path):
    # trange accepts tqdm kwargs; we test that the description is set correctly
    # by inspecting the internal tqdm object's attributes after iteration
    desc = "counting"
    iterator = trange(3, desc=desc)
    # Consume the iterator to trigger tqdm initialization
    list(iterator)
    # The tqdm object is stored in the iterator's internal _tqdm attribute
    # (this is part of the public API of tqdm objects)
    assert iterator._tqdm.desc == desc, "tqdm description should match the provided desc"
    # Ensure the total is set correctly
    assert iterator._tqdm.total == 3, "tqdm total should match the number of iterations"

def test_trange_invalid_input_raises():
    # Passing a non-integer to range should raise a TypeError
    with pytest.raises(TypeError):
        list(trange(1.5, 5))
