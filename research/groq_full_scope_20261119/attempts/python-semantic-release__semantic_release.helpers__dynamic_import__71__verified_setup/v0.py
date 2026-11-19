import importlib
import sys
import types
import os
import pytest
from pathlib import Path

from semantic_release.helpers import dynamic_import


def test_dynamic_import_from_module():
    # Import a known standard library attribute
    result = dynamic_import("math:sqrt")
    assert result is importlib.import_module("math").sqrt
    assert result(4) == 2.0


def test_dynamic_import_from_file(tmp_path):
    # Create a temporary Python file with a simple function
    module_file = tmp_path / "temp_module.py"
    module_file.write_text(
        """
def hello(name: str) -> str:
    return f"Hello, {name}!"
"""
    )
    # Import the function using the file path syntax
    func = dynamic_import(f"{module_file}:{'hello'}")
    assert isinstance(func, types.FunctionType)
    assert func("World") == "Hello, World!"
    # Ensure the module is cached in sys.modules
    module_name = module_file.stem
    assert module_name in sys.modules
    assert getattr(sys.modules[module_name], "hello") is func


def test_dynamic_import_invalid_format():
    # Missing colon should raise ValueError
    with pytest.raises(ValueError, match="must use 'module:Class' format"):
        dynamic_import("invalid_import_path")
