import importlib
import sys
import types
import os
import pytest
from sanic.helpers import import_string


def test_import_string_module(tmp_path):
    """Importing a module by string returns the module object."""
    # Create a temporary package with a module
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / "mymodule.py"
    mod_file.write_text("value = 42\n")

    # Add the temporary package to sys.path
    sys.path.insert(0, str(tmp_path))
    try:
        mod = import_string("mypkg.mymodule")
        assert isinstance(mod, types.ModuleType)
        assert hasattr(mod, "value")
        assert mod.value == 42
    finally:
        sys.path.pop(0)


def test_import_string_class(tmp_path):
    """Importing a class by string returns an instance of that class."""
    # Create a temporary package with a module containing a class
    pkg_dir = tmp_path / "mypkg2"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / "mymodule2.py"
    mod_file.write_text(
        """
class MyClass:
    def __init__(self):
        self.data = "hello"
"""
    )

    sys.path.insert(0, str(tmp_path))
    try:
        instance = import_string("mypkg2.mymodule2.MyClass")
        assert isinstance(instance, types.SimpleNamespace) or hasattr(instance, "data")
        assert instance.data == "hello"
    finally:
        sys.path.pop(0)


def test_import_string_invalid_path(tmp_path):
    """Providing an invalid path raises ImportError."""
    pkg_dir = tmp_path / "mypkg3"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    sys.path.insert(0, str(tmp_path))
    try:
        with pytest.raises(ImportError):
            import_string("mypkg3.nonexistent_module.ClassName")
    finally:
        sys.path.pop(0)
