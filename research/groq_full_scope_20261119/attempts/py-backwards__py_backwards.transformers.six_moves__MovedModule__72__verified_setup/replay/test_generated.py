import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_default_new_attribute():
    """When new is omitted, it should default to the provided name."""
    module = MovedModule(name="module_a", old="old_path")
    assert module.name == "module_a"
    assert module.new == "module_a"

def test_explicit_new_attribute():
    """When new is provided, it should override the default."""
    module = MovedModule(name="module_b", old="old_path", new="new_path")
    assert module.name == "module_b"
    assert module.new == "new_path"

def test_attribute_mutability_and_isolation():
    """Changing one instance's attributes should not affect another."""
    module1 = MovedModule(name="mod1", old="old1")
    module2 = MovedModule(name="mod2", old="old2", new="new2")
    module1.new = "changed"
    assert module1.new == "changed"
    assert module2.new == "new2"
    assert module1.name == "mod1"
    assert module2.name == "mod2"
