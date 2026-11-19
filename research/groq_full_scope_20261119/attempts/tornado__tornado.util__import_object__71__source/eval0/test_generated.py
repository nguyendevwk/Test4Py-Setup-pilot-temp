import pytest
import importlib
from tornado.util import import_object

def test_import_module_direct():
    # Importing a top‑level module should return the module object
    mod = import_object("math")
    assert mod is importlib.import_module("math")
    assert hasattr(mod, "sqrt")

def test_import_attribute_from_module():
    # Importing an attribute from a module should return the attribute
    attr = import_object("math.sin")
    assert attr is importlib.import_module("math").sin
    assert callable(attr)

def test_import_missing_module_or_attribute():
    # Importing a non‑existent module raises ImportError
    with pytest.raises(ImportError) as excinfo:
        import_object("nonexistent_module")
    assert "No module named nonexistent_module" in str(excinfo.value)

    # Importing a missing attribute from an existing module raises ImportError
    with pytest.raises(ImportError) as excinfo:
        import_object("math.nonexistent_attribute")
    assert "No module named nonexistent_attribute" in str(excinfo.value)
