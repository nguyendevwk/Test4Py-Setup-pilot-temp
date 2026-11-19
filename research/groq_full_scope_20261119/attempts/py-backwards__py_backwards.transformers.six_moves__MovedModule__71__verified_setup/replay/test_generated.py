import pytest
from py_backwards.transformers.six_moves import MovedModule

def test_moved_module_with_explicit_new():
    """When a new name is provided, it should be stored correctly."""
    module = MovedModule(name="module_a", old="module_b", new="module_c")
    assert module.name == "module_a"
    assert module.new == "module_c"

def test_moved_module_default_new():
    """When new is omitted, it defaults to the original name."""
    module = MovedModule(name="module_x", old="module_y")
    assert module.name == "module_x"
    assert module.new == "module_x"

def test_moved_module_attribute_types():
    """Ensure that the attributes are of expected types."""
    module = MovedModule(name="mod", old="old_mod", new="new_mod")
    assert isinstance(module.name, str)
    assert isinstance(module.new, str)
