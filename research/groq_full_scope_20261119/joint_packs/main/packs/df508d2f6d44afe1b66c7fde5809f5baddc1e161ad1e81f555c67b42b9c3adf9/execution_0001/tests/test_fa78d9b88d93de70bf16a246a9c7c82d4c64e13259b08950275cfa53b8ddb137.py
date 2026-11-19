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
    keys = list(d.keys())
    assert set(keys) == {"a", "b"}
    items = list(d.items())
    assert ("a", 1) in items and ("b", 2) in items
    d.update({"c": 3})
    assert d.c == 3
    assert len(d) == 3
