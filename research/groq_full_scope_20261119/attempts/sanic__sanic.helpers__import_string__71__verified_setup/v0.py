import importlib
import sys
import types
import pytest
from sanic.helpers import import_string

def test_import_string_module(tmp_path):
    # Create a temporary module with a simple function
    module_code = """
def hello():
    return "world"
"""
    module_path = tmp_path / "temp_module.py"
    module_path.write_text(module_code)

    # Add tmp_path to sys.path so the module can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        mod = import_string("temp_module")
        assert isinstance(mod, types.ModuleType)
        assert hasattr(mod, "hello")
        assert mod.hello() == "world"
    finally:
        sys.path.pop(0)

def test_import_string_class(tmp_path):
    # Create a temporary module with a class that has a method
    module_code = """
class Greeter:
    def greet(self):
        return "hello"
"""
    module_path = tmp_path / "greeter_module.py"
    module_path.write_text(module_code)

    sys.path.insert(0, str(tmp_path))
    try:
        greeter = import_string("greeter_module.Greeter")
        assert isinstance(greeter, object)
        assert hasattr(greeter, "greet")
        assert greeter.greet() == "hello"
    finally:
        sys.path.pop(0)

def test_import_string_invalid_path():
    # Attempt to import a non-existent module/class
    with pytest.raises(ModuleNotFoundError):
        import_string("nonexistent_module")

    with pytest.raises(AttributeError):
        # Module exists but attribute does not
        import_string("importlib.nonexistent_attribute")
