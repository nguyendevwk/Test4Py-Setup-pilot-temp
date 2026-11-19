import pytest
from flutils.namedtupleutils import to_namedtuple

def test_to_namedtuple_raises_on_list(tmp_path):
    """to_namedtuple should raise TypeError when given a list."""
    with pytest.raises(TypeError) as excinfo:
        to_namedtuple([1, 2, 3])
    assert "list" in str(excinfo.value)
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(excinfo.value)

def test_to_namedtuple_raises_on_dict(tmp_path):
    """to_namedtuple should raise TypeError when given a dict."""
    with pytest.raises(TypeError) as excinfo:
        to_namedtuple({"a": 1, "b": 2})
    assert "dict" in str(excinfo.value)
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(excinfo.value)

def test_to_namedtuple_raises_on_namedtuple(tmp_path):
    """to_namedtuple should raise TypeError when given a NamedTuple instance."""
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])
    pt = Point(1, 2)
    with pytest.raises(TypeError) as excinfo:
        to_namedtuple(pt)
    assert "NamedTuple" in str(excinfo.value)
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(excinfo.value)
