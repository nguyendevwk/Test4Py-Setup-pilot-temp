import pytest
from flutes.iterator import MapList

def test_maplist_basic_mapping_and_iteration():
    # Basic mapping: square each element
    original = [1, 2, 3, 4]
    ml = MapList(lambda x: x * x, original)
    # Length matches underlying list
    assert len(ml) == 4
    # Indexing returns transformed value
    assert ml[0] == 1
    assert ml[2] == 9
    # Iteration yields transformed values in order
    assert list(ml) == [1, 4, 9, 16]
    # Underlying list mutation is reflected
    original.append(5)
    assert len(ml) == 5
    assert ml[4] == 25
    assert list(ml) == [1, 4, 9, 16, 25]

def test_maplist_slicing_and_negative_index():
    data = ['a', 'b', 'c', 'd', 'e']
    ml = MapList(str.upper, data)
    # Slice returns list of transformed elements
    assert ml[1:4] == ['B', 'C', 'D']
    # Negative index works as in normal sequence
    assert ml[-1] == 'E'
    # Slice with step
    assert ml[::2] == ['A', 'C', 'E']
    # Slice beyond bounds does not raise error
    assert ml[3:10] == ['D', 'E']
    # Negative slice bounds
    assert ml[-4:-1] == ['B', 'C', 'D']

def test_maplist_error_conditions():
    # Accessing out-of-range index raises IndexError
    ml = MapList(lambda x: x, [1, 2])
    with pytest.raises(IndexError):
        _ = ml[5]
    # Passing a non-sequence to constructor should raise TypeError
    with pytest.raises(TypeError):
        MapList(lambda x: x, 42)  # 42 is not a Sequence
    # Function that raises inside mapping propagates exception
    def bad_func(x):
        if x == 3:
            raise ValueError("bad value")
        return x
    ml_bad = MapList(bad_func, [1, 2, 3, 4])
    # Iteration stops at exception
    with pytest.raises(ValueError, match="bad value"):
        list(ml_bad)
