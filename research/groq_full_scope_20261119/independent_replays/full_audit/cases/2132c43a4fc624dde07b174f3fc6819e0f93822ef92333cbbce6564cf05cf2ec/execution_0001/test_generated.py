import importlib
import sys
import types
import os
import pytest
from pathlib import Path

from semantic_release.helpers import dynamic_import


def test_dynamic_import_from_module():
    """Import a built‑in module attribute correctly."""
    # Import the 'join' function from os.path
    join_func = dynamic_import("os.path:join")
    assert join_func is os.path.join
    # Verify it works as expected
    assert join_func("a", "b") == os.path.join("a", "b")


def test_dynamic_import_from_file(tmp_path):
    """Import an attribute from a temporary module file."""
    # Create a temporary Python file with a simple function
    module_file = tmp_path / "temp_mod.py"
    module_file.write_text(
        """
def hello(name: str) -> str:
    return f"Hello, {name}!"
"""
    )
    # Import the function using the file path
    hello_func = dynamic_import(f"{module_file}:hello")
    # The function should be callable and return the expected string
    assert hello_func("world") == "Hello, world!"
    # Ensure the module was added to sys.modules with the correct name
    module_name = module_file.stem
    assert module_name in sys.modules
    assert getattr(sys.modules[module_name], "hello") is hello_func


def test_dynamic_import_invalid_format():
    """Importing with an invalid format raises ValueError."""
    with pytest.raises(ValueError, match="must use 'module:Class' format"):
        dynamic_import("invalid_format")
