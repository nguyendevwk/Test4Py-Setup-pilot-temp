import pytest
from tornado.util import ObjectDict

def test_attribute_access_and_setting():
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
    with pytest.raises(AttributeError) as exc:
        _ = d.nonexistent
    assert str(exc.value) == "nonexistent"

def test_dict_methods_and_attribute_interaction():
    d = ObjectDict()
    d.a = 1
    d.b = 2
    keys = set(d.keys())
    assert keys == {"a", "b"}
    items = dict(d.items())
    assert items == {"a": 1, "b": 2}
    d.update({"c": 3})
    assert d.c == 3
    del d["a"]
    with pytest.raises(AttributeError):
        _ = d.a
