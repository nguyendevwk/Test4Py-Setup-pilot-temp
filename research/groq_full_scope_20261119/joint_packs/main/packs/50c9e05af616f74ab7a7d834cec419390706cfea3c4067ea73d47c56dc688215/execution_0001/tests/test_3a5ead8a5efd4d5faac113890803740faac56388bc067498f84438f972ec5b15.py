import pytest
from py_backwards.transformers.six_moves import MovedAttribute

def test_full_initialization_sets_all_attributes():
    """When all parameters are supplied, the instance stores them unchanged."""
    attr = MovedAttribute(
        name="foo",
        old_mod="old_pkg",
        new_mod="new_pkg",
        old_attr="old_name",
        new_attr="new_name",
    )
    assert attr.name == "foo"
    assert attr.new_mod == "new_pkg"
    assert attr.new_attr == "new_name"

def test_default_new_mod_and_new_attr_when_none_and_old_attr_missing():
    """If new_mod is None and old_attr is missing, new_mod defaults to name and new_attr defaults to name."""
    attr = MovedAttribute(name="bar", old_mod="old_pkg", new_mod=None)
    assert attr.new_mod == "bar"
    assert attr.new_attr == "bar"

def test_new_attr_defaults_to_old_attr_when_new_mod_provided_and_new_attr_missing():
    """When new_mod is provided but new_attr is omitted, it defaults to old_attr if given, otherwise to name."""
    attr = MovedAttribute(name="baz", old_mod="old_pkg", new_mod="new_pkg", old_attr="old_baz")
    assert attr.new_mod == "new_pkg"
    assert attr.new_attr == "old_baz"
