import pytest
from tornado.util import ObjectDict

def test_attribute_access_and_mutation():
    d = ObjectDict()
    d.foo = 42
    assert d["foo"] == 42
    assert d.foo == 42
    d["bar"] = "baz"
    assert d.bar == "baz"
    d.bar = "qux"
    assert d["bar"] == "qux"

def test_missing_attribute_raises_attributeerror():
    d = ObjectDict()
    d["existing"] = 1
    assert d.existing == 1
    with pytest.raises(AttributeError) as excinfo:
        _ = d.nonexistent
    assert str(excinfo.value) == "nonexistent"

def test_dict_methods_and_iteration():
    d = ObjectDict({"a": 1, "b": 2})
    assert list(d.keys()) == ["a", "b"]
    assert list(d.values()) == [1, 2]
    assert list(d.items()) == [("a", 1), ("b", 2)]
    d.c = 3
    assert d["c"] == 3
    assert set(d) == {"a", "b", "c"}
