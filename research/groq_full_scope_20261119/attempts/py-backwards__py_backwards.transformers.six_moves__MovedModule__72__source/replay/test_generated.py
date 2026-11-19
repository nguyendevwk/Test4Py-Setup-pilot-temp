import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_default_new_attribute():
    """When new is not provided, it defaults to the original name."""
    module = MovedModule(name="foo", old="bar")
    assert module.name == "foo"
    assert module.new == "foo"

def test_custom_new_attribute():
    """When new is provided, it should override the default."""
    module = MovedModule(name="foo", old="bar", new="baz")
    assert module.name == "foo"
    assert module.new == "baz"

def test_attribute_mutability_and_identity():
    """Attributes should be mutable and reflect changes."""
    module = MovedModule(name="alpha", old="beta")
    module.name = "gamma"
    module.new = "delta"
    assert module.name == "gamma"
    assert module.new == "delta"
