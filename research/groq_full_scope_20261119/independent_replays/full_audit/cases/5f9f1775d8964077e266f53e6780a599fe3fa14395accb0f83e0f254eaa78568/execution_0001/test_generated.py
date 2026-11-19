import pytest
from py_backwards.transformers.six_moves import MovedAttribute

def test_default_new_module_and_attribute():
    # When new_mod is None, it defaults to the name
    # When new_attr is None and old_attr is None, it defaults to the name
    ma = MovedAttribute(name="foo", old_mod="old_pkg", new_mod=None, old_attr=None, new_attr=None)
    assert ma.name == "foo"
    assert ma.new_mod == "foo"
    assert ma.new_attr == "foo"

def test_provided_new_module_and_attribute():
    # When new_mod and new_attr are provided, they are used directly
    ma = MovedAttribute(name="bar", old_mod="old_pkg", new_mod="new_pkg", old_attr="old_bar", new_attr="new_bar")
    assert ma.name == "bar"
    assert ma.new_mod == "new_pkg"
    assert ma.new_attr == "new_bar"

def test_old_attr_used_when_new_attr_missing():
    # When new_attr is None but old_attr is provided, new_attr defaults to old_attr
    ma = MovedAttribute(name="baz", old_mod="old_pkg", new_mod="new_pkg", old_attr="old_baz", new_attr=None)
    assert ma.name == "baz"
    assert ma.new_mod == "new_pkg"
    assert ma.new_attr == "old_baz"
