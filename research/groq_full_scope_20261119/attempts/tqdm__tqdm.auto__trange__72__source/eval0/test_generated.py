import pytest
from tqdm.auto import trange

def test_trange_normal_iteration():
    """trange should iterate over the given range and yield the same values."""
    result = list(trange(5, desc="count"))
    assert result == [0, 1, 2, 3, 4]
    # The progress bar should have been created with the provided description
    # (the tqdm object is not directly exposed, but we can check that the
    # description attribute is set on the iterator returned by trange).
    # Since trange returns a tqdm instance, we can access its `desc` attribute.
    progress_bar = trange(5, desc="count")
    assert progress_bar.desc == "count"

def test_trange_zero_length():
    """trange with a zero-length range should produce an empty iterator."""
    result = list(trange(0))
    assert result == []

def test_trange_name_error():
    """trange should raise NameError because tqdm is not defined in the module."""
    with pytest.raises(NameError):
        list(trange(3))
