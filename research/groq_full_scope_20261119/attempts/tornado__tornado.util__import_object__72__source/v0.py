import pytest
from tornado.util import import_object

def test_import_object_basic_module():
    # Import a top‑level module and verify identity
    mod = import_object("math")
    import math
    assert mod is math
    # Import a submodule and verify identity
    submod = import_object("tornado.escape")
    import tornado.escape
    assert submod is tornado.escape

def test_import_object_attribute():
    # Import a specific attribute from a module
    utf8_func = import_object("tornado.escape.utf8")
    from tornado.escape import utf8
    assert utf8_func is utf8
    # Import a class from a submodule
    json_module = import_object("json.decoder.JSONDecoder")
    from json.decoder import JSONDecoder
    assert json_module is JSONDecoder

def test_import_object_errors():
    # Importing a non‑existent module should raise ImportError
    with pytest.raises(ImportError) as excinfo:
        import_object("nonexistent_module")
    assert "No module named nonexistent_module" in str(excinfo.value)

    # Importing a non‑existent attribute from an existing module
    with pytest.raises(ImportError) as excinfo:
        import_object("math.nonexistent_attribute")
    assert "No module named nonexistent_attribute" in str(excinfo.value)
