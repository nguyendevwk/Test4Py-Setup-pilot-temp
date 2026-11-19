import importlib
import sys
import types
import pytest
from sanic.helpers import import_string

def test_import_string_module(tmp_path):
    # Create a temporary module with a simple function
    mod_path = tmp_path / "temp_mod.py"
    mod_path.write_text("def hello():\n    return 'world'\n")
    sys.path.insert(0, str(tmp_path))
    try:
        mod = import_string("temp_mod")
        assert isinstance(mod, types.ModuleType)
        assert hasattr(mod, "hello")
        assert mod.hello() == "world"
    finally:
        sys.path.pop(0)

def test_import_string_class(tmp_path):
    # Create a temporary module with a class that returns a value
    mod_path = tmp_path / "temp_cls.py"
    mod_path.write_text(
        "class Greeter:\n"
        "    def __init__(self):\n"
        "        self.message = 'hi'\n"
        "    def greet(self):\n"
        "        return self.message\n"
    )
    sys.path.insert(0, str(tmp_path))
    try:
        instance = import_string("temp_cls.Greeter")
        assert hasattr(instance, "greet")
        assert instance.greet() == "hi"
    finally:
        sys.path.pop(0)

def test_import_string_invalid_path():
    # Importing a non‑existent module or attribute should raise ImportError
    with pytest.raises(ImportError):
        import_string("nonexistent.module")
    with pytest.raises(AttributeError):
        import_string("math.nonexistent_attribute")
