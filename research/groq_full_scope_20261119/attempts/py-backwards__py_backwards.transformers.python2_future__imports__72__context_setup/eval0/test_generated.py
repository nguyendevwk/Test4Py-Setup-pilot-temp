import importlib
import sys
import types

import pytest

# Import the target function
from py_backwards.transformers.python2_future import imports


def _module_present(name: str) -> bool:
    """Check if a module is present in sys.modules."""
    return name in sys.modules


def _remove_module(name: str):
    """Remove a module from sys.modules if it exists."""
    sys.modules.pop(name, None)


@pytest.fixture(autouse=True)
def cleanup_modules():
    """Ensure that future modules are removed after each test."""
    yield
    for mod in ("future.absolute_import", "future.division",
                "future.print_function", "future.unicode_literals"):
        _remove_module(mod)


def test_imports_success():
    """Calling imports should load all required future modules."""
    imports(None)  # argument is ignored
    assert _module_present("future.absolute_import")
    assert _module_present("future.division")
    assert _module_present("future.print_function")
    assert _module_present("future.unicode_literals")
    # Verify that the modules are actual module objects
    for mod_name in ("future.absolute_import", "future.division",
                     "future.print_function", "future.unicode_literals"):
        assert isinstance(sys.modules[mod_name], types.ModuleType)


def test_imports_idempotent():
    """Calling imports multiple times should not raise and keep modules loaded."""
    imports(None)
    first_ids = {name: id(sys.modules[name]) for name in sys.modules}
    imports(None)
    second_ids = {name: id(sys.modules[name]) for name in sys.modules}
    # The module objects should be the same after the second call
    for name in ("future.absolute_import", "future.division",
                 "future.print_function", "future.unicode_literals"):
        assert first_ids[name] == second_ids[name]


def test_imports_with_invalid_argument():
    """The imports function ignores its argument; passing a non-module should still work."""
    class Dummy:  # arbitrary object
        pass
    imports(Dummy())
    # Modules should still be present
    assert _module_present("future.absolute_import")
    assert _module_present("future.division")
    assert _module_present("future.print_function")
    assert _module_present("future.unicode_literals")
