import importlib
import sys
import types
import pytest

# Import the target function
from py_backwards.transformers.python2_future import imports


def test_imports_success():
    """
    Verify that calling imports() successfully imports the expected future modules
    and that they are present in sys.modules.
    """
    # Ensure modules are not already imported
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        sys.modules.pop(mod, None)

    # Call the function
    result = imports(None)

    # The function should return None
    assert result is None

    # Check that each module is now imported
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod in sys.modules
        assert isinstance(sys.modules[mod], types.ModuleType)


def test_imports_idempotent(monkeypatch):
    """
    Verify that calling imports() multiple times does not raise errors
    and does not alter the modules after the first import.
    """
    # Import once
    imports(None)
    first_modules = {k: v for k, v in sys.modules.items()
                     if k.startswith("future.")}

    # Call again
    imports(None)
    second_modules = {k: v for k, v in sys.modules.items()
                      if k.startswith("future.")}

    # The module objects should be the same
    assert first_modules == second_modules
    # No new modules should appear
    assert set(first_modules.keys()) == set(second_modules.keys())


def test_imports_missing_future_module(monkeypatch):
    """
    Simulate the absence of the 'future' package and verify that imports()
    raises ImportError.
    """
    # Remove the 'future' package from sys.modules if present
    monkeypatch.setitem(sys.modules, "future", None)

    # Ensure importlib cannot find the package
    def fake_import(name, *args, **kwargs):
        if name == "future":
            raise ImportError("No module named 'future'")
        return importlib.import_module(name, *args, **kwargs)

    monkeypatch.setattr(importlib, "import_module", fake_import)

    # Calling imports should raise ImportError
    with pytest.raises(ImportError, match="No module named 'future'"):
        imports(None)
