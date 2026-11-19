import pytest
from py_backwards.transformers.six_moves import MovedAttribute

def test_full_parameters():
    """All parameters provided explicitly."""
    attr = MovedAttribute(
        name="foo",
        old_mod="old_module",
        new_mod="new_module",
        old_attr="old_attr",
        new_attr="new_attr",
    )
    assert attr.name == "foo"
    assert attr.old_mod == "old_module"
    assert attr.new_mod == "new_module"
    assert attr.new_attr == "new_attr"

def test_default_new_mod_and_new_attr():
    """new_mod and new_attr default to name when omitted."""
    attr = MovedAttribute(name="bar", old_mod="old_module", new_mod=None)
    assert attr.name == "bar"
    assert attr.old_mod == "old_module"
    assert attr.new_mod == "bar"          # defaulted to name
    assert attr.new_attr == "bar"         # defaulted to name

def test_new_attr_from_old_attr_when_new_mod_none():
    """new_attr defaults to old_attr when new_mod is None and old_attr is provided."""
    attr = MovedAttribute(
        name="baz",
        old_mod="old_module",
        new_mod=None,
        old_attr="old_attr",
        new_attr=None,
    )
    assert attr.name == "baz"
    assert attr.old_mod == "old_module"
    assert attr.new_mod == "baz"          # defaulted to name
    assert attr.new_attr == "old_attr"    # taken from old_attr

def test_missing_required_argument_raises():
    """Calling without required arguments should raise TypeError."""
    with pytest.raises(TypeError):
        MovedAttribute("name", "old_module")  # missing new_mod argument
