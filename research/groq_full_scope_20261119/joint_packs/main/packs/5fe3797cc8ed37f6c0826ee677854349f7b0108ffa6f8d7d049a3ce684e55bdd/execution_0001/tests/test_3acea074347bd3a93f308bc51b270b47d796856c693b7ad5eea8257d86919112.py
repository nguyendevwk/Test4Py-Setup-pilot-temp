import pytest
from tornado.util import ObjectDict

def test_attribute_access_and_setting():
    d = ObjectDict()
    d.foo = 42
    assert d["foo"] == 42
    assert d.foo == 42
    d["bar"] = "baz"
    assert d.bar == "baz"
    d.qux = [1, 2, 3]
    assert d["qux"] == [1, 2, 3]
    assert isinstance(d.qux, list)

def test_attribute_error_on_missing_key():
    d = ObjectDict()
    d.existing = "value"
    with pytest.raises(AttributeError) as excinfo:
        _ = d.nonexistent
    assert "nonexistent" in str(excinfo.value)

def test_dict_methods_and_attribute_interaction():
    d = ObjectDict({"a": 1, "b": 2})
    assert d.get("a") == 1
    assert d.get("missing", "default") == "default"
    d.update({"c": 3})
    assert d.c == 3
    d.pop("b")
    assert "b" not in d
    with pytest.raises(KeyError):
        d.pop("nonexistent")
