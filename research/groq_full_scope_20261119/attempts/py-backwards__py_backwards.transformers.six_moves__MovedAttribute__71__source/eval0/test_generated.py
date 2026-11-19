import pytest
from py_backwards.transformers.six_moves import MovedAttribute

def test_default_new_mod_and_attr():
    """When new_mod and new_attr are omitted, they default to the name."""
    attr = MovedAttribute(name="foo", old_mod="old_pkg")
    assert attr.name == "foo"
    assert attr.new_mod == "foo"          # default to name
    assert attr.new_attr == "foo"         # default to name

def test_provided_new_mod_and_attr():
    """When new_mod and new_attr are explicitly provided, they are used."""
    attr = MovedAttribute(name="bar", old_mod="old_pkg", new_mod="new_pkg", new_attr="baz")
    assert attr.name == "bar"
    assert attr.new_mod == "new_pkg"
    assert attr.new_attr == "baz"

def test_old_attr_only():
    """When only old_attr is provided, new_attr defaults to old_attr."""
    attr = MovedAttribute(name="qux", old_mod="old_pkg", old_attr="old_name")
    assert attr.name == "qux"
    assert attr.new_mod == "qux"          # default to name
    assert attr.new_attr == "old_name"    # uses old_attr
