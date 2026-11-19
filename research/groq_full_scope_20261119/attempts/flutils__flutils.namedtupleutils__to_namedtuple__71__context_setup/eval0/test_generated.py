import pytest
from flutils.namedtupleutils import to_namedtuple
from collections import namedtuple, OrderedDict
from types import SimpleNamespace

def test_to_namedtuple_raises_on_list():
    """to_namedtuple should raise TypeError when given a plain list."""
    with pytest.raises(TypeError) as exc:
        to_namedtuple([1, 2, 3])
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(exc.value)

def test_to_namedtuple_raises_on_tuple():
    """to_namedtuple should raise TypeError when given a plain tuple."""
    with pytest.raises(TypeError) as exc:
        to_namedtuple((1, 2, 3))
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(exc.value)

def test_to_namedtuple_raises_on_dict():
    """to_namedtuple should raise TypeError when given a plain dict."""
    with pytest.raises(TypeError) as exc:
        to_namedtuple({"a": 1, "b": 2})
    assert "Can convert only 'list', 'tuple', 'dict' to a NamedTuple" in str(exc.value)
