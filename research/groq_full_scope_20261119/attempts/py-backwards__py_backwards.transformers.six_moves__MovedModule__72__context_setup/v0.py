import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_moved_module_with_explicit_new():
    """When a new name is provided, it should be stored unchanged."""
    module = MovedModule(name="foo", old="bar", new="baz")
    assert module.name == "foo"
    assert module.new == "baz"

def test_moved_module_default_new():
    """When new is omitted, it defaults to the original name."""
    module = MovedModule(name="alpha", old="beta")
    assert module.name == "alpha"
    assert module.new == "alpha"

def test_moved_module_attribute_mutation():
    """Attributes can be mutated after creation and reflect the new values."""
    module = MovedModule(name="x", old="y")
    module.name = "new_name"
    module.new = "new_new"
    assert module.name == "new_name"
    assert module.new == "new_new"
