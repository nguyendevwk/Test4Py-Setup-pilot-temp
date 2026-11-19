import os
import types
import pytest
from pathlib import Path
from sanic.utils import load_module_from_file_location, LoadFileException, PyFileError


def test_load_python_module_from_file(tmp_path):
    """Test loading a .py file and accessing its attributes."""
    # Create a simple Python module file
    module_path = tmp_path / "sample.py"
    module_path.write_text("value = 42\n", encoding="utf8")

    # Load the module
    mod = load_module_from_file_location(str(module_path))

    # Verify that the module is a types.ModuleType and contains the expected attribute
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "value")
    assert mod.value == 42


def test_load_config_with_env_var(tmp_path):
    """Test that environment variables in the path are substituted correctly."""
    # Set an environment variable
    os.environ["TEST_ENV"] = "env_value"

    # Create a config file that will be loaded as a module
    config_path = tmp_path / "config.cfg"
    config_path.write_text("config_value = 'ok'\n", encoding="utf8")

    # Path with environment variable placeholder
    path_with_env = f"{tmp_path}/${{TEST_ENV}}/config.cfg"
    # Create the directory referenced by the env var
    (tmp_path / "env_value").mkdir()
    # Copy the config file into the env directory
    (tmp_path / "env_value" / "config.cfg").write_text("config_value = 'ok'\n", encoding="utf8")

    # Load the module using the path with the env variable
    mod = load_module_from_file_location(path_with_env)

    # Verify that the module was loaded from the substituted path
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "config_value")
    assert mod.config_value == "ok"


def test_load_nonexistent_file_raises_pyfileerror(tmp_path):
    """Test that loading a non‑existent file raises PyFileError."""
    nonexistent_path = tmp_path / "does_not_exist.cfg"

    with pytest.raises(PyFileError) as excinfo:
        load_module_from_file_location(str(nonexistent_path))

    # The exception should reference the path that was attempted
    assert str(nonexistent_path) in str(excinfo.value)
