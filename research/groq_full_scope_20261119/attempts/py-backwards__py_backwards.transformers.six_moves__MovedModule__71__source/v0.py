import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_moved_module_with_explicit_new_name():
    """When a new name is provided, it should be stored correctly."""
    module = MovedModule(name="old_module", old="old_path", new="new_module")
    assert module.name == "old_module"
    assert module.new == "new_module"

def test_moved_module_default_new_name():
    """When new is None, it should default to the original name."""
    module = MovedModule(name="module_name", old="old_path")
    assert module.name == "module_name"
    assert module.new == "module_name"

def test_moved_module_with_non_string_new():
    """The class does not enforce type; it should accept any value for new."""
    module = MovedModule(name="mod", old="old_path", new=42)
    assert module.name == "mod"
    assert module.new == 42
