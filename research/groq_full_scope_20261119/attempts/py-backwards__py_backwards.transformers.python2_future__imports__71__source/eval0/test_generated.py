import sys
import importlib
import pytest

# Import the target function from the package
from py_backwards.transformers.python2_future import imports


def test_imports_success():
    """
    Verify that calling imports() loads the expected future modules
    into sys.modules without raising an exception.
    """
    # Ensure the modules are not already loaded
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod not in sys.modules

    # Call the function
    imports(None)

    # Check that each module is now present
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod in sys.modules
        # The module should be importable via importlib
        assert importlib.import_module(mod) is sys.modules[mod]


def test_imports_idempotent():
    """
    Calling imports() multiple times should not raise errors and
    should not alter the modules after the first import.
    """
    imports(None)
    first_state = {k: sys.modules[k] for k in sys.modules if k.startswith("future.")}

    # Call again
    imports(None)
    second_state = {k: sys.modules[k] for k in sys.modules if k.startswith("future.")}

    # The state should be identical
    assert first_state == second_state


def test_imports_argument_ignored():
    """
    The function accepts any argument but ignores it; passing a
    non-None value should still result in the same imports.
    """
    imports("some_string")
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        assert mod in sys.modules
