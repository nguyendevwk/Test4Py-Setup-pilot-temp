import pytest
from pysnooper import variables

# Import the classes that Exploding delegates to
Keys = variables.Keys
Indices = variables.Indices
Attrs = variables.Attrs
Exploding = variables.Exploding

class DummySource:
    """A minimal source object that records the last call."""
    def __init__(self):
        self.last_call = None

    def record(self, value):
        self.last_call = value

def test_exploding_mapping_returns_keys(tmp_path):
    """Exploding should delegate to Keys for mapping objects."""
    source = DummySource()
    exploding = Exploding(source, exclude=[])
    mapping = {"a": 1, "b": 2}
    result = exploding._items(mapping, normalize=False)
    # Keys._items should return the mapping's keys
    assert set(result) == {"a", "b"}
    # The source should have recorded the mapping
    assert source.last_call == mapping

def test_exploding_sequence_returns_indices(tmp_path):
    """Exploding should delegate to Indices for sequence objects."""
    source = DummySource()
    exploding = Exploding(source, exclude=[])
    seq = [10, 20, 30]
    result = exploding._items(seq, normalize=True)
    # Indices._items should return the indices of the sequence
    assert result == [0, 1, 2]
    # The source should have recorded the sequence
    assert source.last_call == seq

def test_exploding_object_returns_attrs(tmp_path):
    """Exploding should delegate to Attrs for non-mapping, non-sequence objects."""
    source = DummySource()
    exploding = Exploding(source, exclude=[])
    class Sample:
        x = 5
        y = "hello"
    obj = Sample()
    result = exploding._items(obj, normalize=False)
    # Attrs._items should return the object's attributes
    assert set(result) == {"x", "y"}
    # The source should have recorded the object
    assert source.last_call == obj
