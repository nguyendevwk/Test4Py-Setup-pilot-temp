import pytest
from pysnooper.variables import Exploding
from collections.abc import Mapping, Sequence

class Dummy:
    a = 1
    b = 2

def test_exploding_mapping():
    """Exploding should delegate to Keys for mapping objects."""
    data = {"x": 10, "y": 20}
    expl = Exploding(source="test", exclude=[])
    result = expl._items(data)
    # Keys._items should return a list of (key, value) tuples
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    assert set(result) == {("x", 10), ("y", 20)}

def test_exploding_sequence():
    """Exploding should delegate to Indices for sequence objects."""
    data = [100, 200, 300]
    expl = Exploding(source="test", exclude=[])
    result = expl._items(data)
    # Indices._items should return a list of (index, value) tuples
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    assert result == [(0, 100), (1, 200), (2, 300)]

def test_exploding_object_attributes():
    """Exploding should delegate to Attrs for non-mapping, non-sequence objects."""
    obj = Dummy()
    expl = Exploding(source="test", exclude=[])
    result = expl._items(obj)
    # Attrs._items should return a list of (attribute_name, value) tuples
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)
    # Only public attributes should be present
    attrs = {name: getattr(obj, name) for name in dir(obj) if not name.startswith("_")}
    assert set(result) == set(attrs.items())
