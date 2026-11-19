import importlib
import sys
import types
import os
import pytest
from pathlib import Path

from semantic_release.helpers import dynamic_import


def test_dynamic_import_from_module(tmp_path):
    """Import a function from a standard module."""
    # Create a temporary package with a module
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / "mymod.py"
    mod_file.write_text("def hello():\n    return 'world'\n")

    # Add package to sys.path so it can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        func = dynamic_import("mypkg.mymod:hello")
        assert callable(func)
        assert func() == "world"
    finally:
        sys.path.pop(0)


def test_dynamic_import_from_file(tmp_path):
    """Import a class from a file path using the file:attribute syntax."""
    # Create a temporary module file
    mod_file = tmp_path / "temp_module.py"
    mod_file.write_text(
        "class Greeter:\n"
        "    def greet(self, name):\n"
        "        return f'Hello, {name}!'\n"
    )

    # Use the absolute path to the file
    import_path = f"{mod_file.resolve()}:Greeter"
    Greeter = dynamic_import(import_path)
    assert isinstance(Greeter, type)
    greeter = Greeter()
    assert greeter.greet("Alice") == "Hello, Alice!"


def test_dynamic_import_invalid_format():
    """Importing with an invalid format should raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        dynamic_import("invalidformat")
    assert "must use 'module:Class'" in str(excinfo.value)
