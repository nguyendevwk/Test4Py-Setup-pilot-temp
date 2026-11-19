import itertools
import pytest
from tqdm.contrib.itertools import chain
from tqdm.auto import tqdm as tqdm_auto


def test_chain_with_len_and_total():
    """When all iterables support len, total is computed automatically."""
    a = [1, 2, 3]
    b = [4, 5]
    # chain should iterate over all elements in order
    result = list(chain(a, b))
    assert result == [1, 2, 3, 4, 5]

    # The returned tqdm object should have the correct total
    # We can access the internal iterator to check the total attribute
    # Since chain returns tqdm_auto, its .total attribute is set
    # We create a new chain to inspect the tqdm object directly
    tqdm_obj = chain(a, b)
    assert isinstance(tqdm_obj, tqdm_auto)
    assert tqdm_obj.total == len(a) + len(b)


def test_chain_without_len(tmp_path):
    """When iterables lack __len__, total remains None."""
    # Create a temporary file and iterate over its lines
    file_path = tmp_path / "sample.txt"
    file_path.write_text("line1\nline2\n")
    file_iter = file_path.open("r")

    # Use a list as the second iterable
    lst = [10, 20]

    # Chain the file iterator and the list
    tqdm_obj = chain(file_iter, lst)
    assert isinstance(tqdm_obj, tqdm_auto)
    # Since file_iter has no len, total should be None
    assert tqdm_obj.total is None

    # Consume the chain and verify the output
    result = list(tqdm_obj)
    # file_iter yields lines with newline characters
    assert result == ["line1\n", "line2\n", 10, 20]


def test_chain_error_on_non_iterable():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        # An integer is not iterable; chain should raise when trying to iterate
        list(chain(42, [1, 2, 3]))
