import importlib
import sys
import types

import pytest

# Import the target function from the production code
from py_backwards.transformers.python2_future import imports


def test_imports_successfully_imports_future_modules():
    """Calling imports should load the expected future modules into sys.modules."""
    # Ensure the modules are not already loaded
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        sys.modules.pop(mod, None)

    imports(future=types.SimpleNamespace())  # argument is irrelevant

    # Verify that each module is now present in sys.modules
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod in sys.modules, f"{mod} was not imported"


def test_imports_is_idempotent_and_does_not_raise():
    """Calling imports multiple times should not raise an exception."""
    # First call
    imports(future=types.SimpleNamespace())
    # Second call should be safe
    imports(future=types.SimpleNamespace())
    # No exception means test passes


def test_imports_argument_is_ignored_and_returns_none():
    """The function ignores its argument and returns None."""
    result = imports(future=42)  # arbitrary argument
    assert result is None, "imports should return None regardless of the argument"
