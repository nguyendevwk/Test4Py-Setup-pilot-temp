import pytest
from py_backwards.transformers.six_moves import MovedAttribute


def test_default_new_mod_and_new_attr_when_none():
    """
    When new_mod is None, it should default to the name.
    When old_attr and new_attr are None, new_attr should default to the name.
    """
    ma = MovedAttribute(name="foo", old_mod="old_pkg", new_mod=None)
    assert ma.name == "foo"
    # new_mod defaults to name
    assert ma.new_mod == "foo"
    # new_attr defaults to name because old_attr is None
    assert ma.new_attr == "foo"


def test_old_attr_propagates_to_new_attr_when_new_attr_missing():
    """
    If old_attr is provided and new_attr is omitted, new_attr should be set to old_attr.
    """
    ma = MovedAttribute(name="bar", old_mod="old_pkg", new_mod="new_pkg", old_attr="old_name")
    assert ma.new_mod == "new_pkg"
    # new_attr should copy old_attr
    assert ma.new_attr == "old_name"


def test_explicit_new_attr_overrides_old_attr_and_name():
    """
    When new_attr is explicitly provided, it should override both old_attr and name.
    """
    ma = MovedAttribute(name="baz", old_mod="old_pkg", new_mod="new_pkg",
                        old_attr="old_name", new_attr="explicit_new")
    assert ma.new_mod == "new_pkg"
    # new_attr should be the explicit value
    assert ma.new_attr == "explicit_new"
    # name remains unchanged
    assert ma.name == "baz"
