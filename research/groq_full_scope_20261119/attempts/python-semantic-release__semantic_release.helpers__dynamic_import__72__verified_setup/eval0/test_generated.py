import importlib
import sys
import types
import os
import pytest
from pathlib import Path

from semantic_release.helpers import dynamic_import


def test_dynamic_import_from_module():
    """Import a standard library attribute via module:attribute syntax."""
    # Import the 'pathlib' module and its 'Path' class
    PathCls = dynamic_import("pathlib:Path")
    assert PathCls is Path
    # Ensure the returned object behaves like pathlib.Path
    p = PathCls("test.txt")
    assert isinstance(p, Path)
    assert p.name == "test.txt"


def test_dynamic_import_from_file(tmp_path):
    """Import a function defined in a temporary file using a file path."""
    # Create a temporary Python file with a simple function
    file_path = tmp_path / "mymodule.py"
    file_path.write_text(
        """
def hello(name: str) -> str:
    return f"Hello, {name}!"
"""
    )
    # Import the function via the file path
    hello_func = dynamic_import(f"{file_path}:hello")
    assert callable(hello_func)
    assert hello_func("World") == "Hello, World!"
    # Ensure the module is cached in sys.modules
    module_name = file_path.stem
    assert module_name in sys.modules
    assert sys.modules[module_name].hello is hello_func


def test_dynamic_import_invalid_format():
    """Importing with an invalid format should raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        dynamic_import("invalidformat")
    assert "must use 'module:Class'" in str(excinfo.value)
