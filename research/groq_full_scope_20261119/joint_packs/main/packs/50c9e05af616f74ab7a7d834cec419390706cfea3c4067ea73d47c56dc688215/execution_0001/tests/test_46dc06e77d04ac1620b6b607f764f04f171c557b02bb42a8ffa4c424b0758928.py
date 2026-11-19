import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_default_new_attribute():
    """When new is omitted, it should default to the provided name."""
    module = MovedModule(name="module_a", old="old_module_a")
    assert module.name == "module_a"
    assert module.new == "module_a"

def test_explicit_new_attribute():
    """When new is provided, it should override the default."""
    module = MovedModule(name="module_b", old="old_module_b", new="new_module_b")
    assert module.name == "module_b"
    assert module.new == "new_module_b"

def test_none_new_attribute():
    """Passing new=None explicitly should still default to the name."""
    module = MovedModule(name="module_c", old="old_module_c", new=None)
    assert module.name == "module_c"
    assert module.new == "module_c"
