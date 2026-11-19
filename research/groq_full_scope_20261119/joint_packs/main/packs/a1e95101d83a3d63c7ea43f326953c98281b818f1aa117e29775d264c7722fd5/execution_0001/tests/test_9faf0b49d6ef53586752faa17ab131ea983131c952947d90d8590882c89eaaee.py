import pytest
from flutes.iterator import MapList

def test_maplist_basic_mapping():
    # Map each element to its square
    original = [1, 2, 3, 4]
    mapped = MapList(lambda x: x * x, original)
    # Indexing returns transformed value
    assert mapped[0] == 1
    assert mapped[3] == 16
    # Iteration yields transformed values in order
    assert list(mapped) == [1, 4, 9, 16]
    # Length matches underlying list
    assert len(mapped) == len(original)

def test_maplist_slice_and_sequence_behavior():
    # Map each element to its string representation
    original = ['a', 'b', 'c', 'd']
    mapped = MapList(str.upper, original)
    # Slicing returns a list of transformed values
    assert mapped[1:3] == ['B', 'C']
    # Negative indices work as expected
    assert mapped[-1] == 'D'
    # Full slice returns all transformed values
    assert mapped[:] == ['A', 'B', 'C', 'D']

def test_maplist_index_error():
    # Map a simple identity function
    original = [10, 20]
    mapped = MapList(lambda x: x, original)
    # Accessing an out-of-range index should raise IndexError
    with pytest.raises(IndexError):
        _ = mapped[5]
