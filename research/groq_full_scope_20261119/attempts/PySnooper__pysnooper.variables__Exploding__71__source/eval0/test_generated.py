import pytest
from collections.abc import Mapping, Sequence
from pysnooper.variables import Exploding

# Helper class with attributes for testing
class Dummy:
    def __init__(self):
        self.x = 1
        self.y = 2

def test_exploding_dict_items():
    """Exploding should delegate to Keys for mapping objects."""
    source = {"a": 1, "b": 2}
    expl = Exploding(source, exclude=[])
    # _items should return the keys of the dict
    result = expl._items(source)
    assert isinstance(result, list)
    assert set(result) == {"a", "b"}

def test_exploding_sequence_items():
    """Exploding should delegate to Indices for sequence objects."""
    source = [10, 20, 30]
    expl = Exploding(source, exclude=[])
    # _items should return the indices of the list
    result = expl._items(source)
    assert isinstance(result, list)
    assert result == [0, 1, 2]

def test_exploding_object_attrs():
    """Exploding should delegate to Attrs for non-mapping, non-sequence objects."""
    dummy = Dummy()
    expl = Exploding(dummy, exclude=[])
    # _items should return the attribute names of the object
    result = expl._items(dummy)
    assert isinstance(result, list)
    # The attribute names should include 'x' and 'y'
    assert set(result) == {"x", "y"}
