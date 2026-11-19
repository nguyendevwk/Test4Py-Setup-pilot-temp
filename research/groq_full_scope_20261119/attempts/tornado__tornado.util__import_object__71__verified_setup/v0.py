import pytest
import importlib
from tornado.util import import_object

def test_import_module_success():
    # Import a top-level module and verify identity
    mod = import_object('math')
    assert mod is importlib.import_module('math')
    assert hasattr(mod, 'sqrt')
    assert mod.sqrt(4) == 2.0

def test_import_attribute_success():
    # Import a specific attribute from a module
    utf8_func = import_object('tornado.escape.utf8')
    assert utf8_func is importlib.import_module('tornado.escape').utf8
    # Verify the function works as expected
    assert utf8_func('hello') == b'hello'

def test_import_missing_module_or_attribute():
    # Importing a non-existent module should raise ImportError
    with pytest.raises(ImportError) as excinfo_mod:
        import_object('nonexistent_module')
    assert "No module named nonexistent_module" in str(excinfo_mod.value)

    # Importing a non-existent attribute from an existing module should raise ImportError
    with pytest.raises(ImportError) as excinfo_attr:
        import_object('math.nonexistent_attribute')
    assert "No module named nonexistent_attribute" in str(excinfo_attr.value)
