import pytest
from py_backwards.transformers.six_moves import MovedAttribute


def test_default_new_mod_and_attr():
    """
    When new_mod is None, it should default to the name.
    When new_attr is None and old_attr is None, it should default to the name.
    """
    ma = MovedAttribute(name="foo", old_mod="old_pkg", new_mod=None)
    assert ma.name == "foo"
    assert ma.old_mod == "old_pkg"
    # new_mod defaults to name
    assert ma.new_mod == "foo"
    # new_attr defaults to name
    assert ma.new_attr == "foo"


def test_custom_new_mod_and_attr():
    """
    When new_mod and new_attr are explicitly provided, they should be used.
    """
    ma = MovedAttribute(
        name="bar",
        old_mod="old_pkg",
        new_mod="new_pkg",
        old_attr="old_bar",
        new_attr="new_bar",
    )
    assert ma.name == "bar"
    assert ma.old_mod == "old_pkg"
    assert ma.new_mod == "new_pkg"
    assert ma.new_attr == "new_bar"
    # old_attr is not stored, but we can check that new_attr is not affected by old_attr
    assert ma.new_attr != "old_bar"


def test_old_attr_propagation_when_new_attr_missing():
    """
    When new_attr is None but old_attr is provided, new_attr should be set to old_attr.
    """
    ma = MovedAttribute(name="baz", old_mod="old_pkg", new_mod="new_pkg", old_attr="old_baz")
    assert ma.new_attr == "old_baz"
    # Ensure that new_mod is still correctly set
    assert ma.new_mod == "new_pkg"
