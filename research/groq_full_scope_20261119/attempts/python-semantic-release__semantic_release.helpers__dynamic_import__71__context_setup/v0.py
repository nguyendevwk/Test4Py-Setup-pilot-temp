import importlib
import sys
import types
import os
import tempfile
import textwrap
import pytest

from semantic_release.helpers import dynamic_import


def test_dynamic_import_from_module(tmp_path):
    # Create a temporary package with a module and a function
    pkg_dir = tmp_path / "mypkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    mod_file = pkg_dir / "mymod.py"
    mod_file.write_text(textwrap.dedent("""
        def hello(name):
            return f"Hello, {name}!"
    """))
    # Add package to sys.path so it can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        # Import the function via dynamic_import
        func = dynamic_import("mypkg.mymod:hello")
        assert callable(func)
        assert func("World") == "Hello, World!"
    finally:
        sys.path.pop(0)


def test_dynamic_import_from_file(tmp_path):
    # Create a standalone module file
    mod_file = tmp_path / "standalone.py"
    mod_file.write_text(textwrap.dedent("""
        class Greeter:
            def greet(self, name):
                return f"Hi, {name}!"
    """))
    # Import the class via a file path
    cls = dynamic_import(f"{mod_file}:Greeter")
    assert cls.__name__ == "Greeter"
    instance = cls()
    assert instance.greet("Alice") == "Hi, Alice!"


def test_dynamic_import_invalid_path_raises():
    # Missing colon should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        dynamic_import("invalidpath")
    assert "must use 'module:Class'" in str(excinfo.value)

    # Non-existent module should raise ImportError
    with pytest.raises(ImportError):
        dynamic_import("nonexistentmodule:Something")
