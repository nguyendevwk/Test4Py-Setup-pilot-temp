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
    # Ensure the modules are not already imported
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
    Verify that calling imports() multiple times does not raise an exception
    and does not alter the modules after the first import.
    """
    # Import once
    imports(None)
    first_modules = set(sys.modules.keys())

    # Call again
    imports(None)
    second_modules = set(sys.modules.keys())

    # The set of modules should be unchanged
    assert first_modules == second_modules

    # Ensure the specific future modules are still present
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod in sys.modules


def test_imports_missing_future(monkeypatch):
    """
    Verify that if the 'future' package is not available, imports() raises ImportError.
    """
    # Temporarily remove 'future' from sys.modules and from sys.path
    original_future = sys.modules.pop("future", None)
    original_path = sys.path.copy()
    sys.path = [p for p in sys.path if "future" not in p]

    # Ensure that importing future fails
    with pytest.raises(ImportError):
        imports(None)

    # Restore original state
    if original_future is not None:
        sys.modules["future"] = original_future
    sys.path = original_path
