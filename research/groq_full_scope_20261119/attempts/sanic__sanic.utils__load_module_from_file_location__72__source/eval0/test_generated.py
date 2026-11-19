import os
import types
import pytest
from pathlib import Path

from sanic.utils import load_module_from_file_location, LoadFileException, PyFileError


def test_load_python_module_from_file(tmp_path):
    # Create a simple Python file
    py_file = tmp_path / "sample.py"
    py_file.write_text("x = 42\n")
    # Load the module
    mod = load_module_from_file_location(str(py_file))
    # Assert that the module has the expected attribute
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "x")
    assert mod.x == 42


def test_load_config_with_env_var(tmp_path):
    # Set an environment variable
    os.environ["TEST_ENV"] = "value_from_env"
    # Create a config file that uses the env var
    cfg_file = tmp_path / "config.cfg"
    cfg_file.write_text("data = '${TEST_ENV}'\n")
    # Load the config
    mod = load_module_from_file_location(str(cfg_file))
    # The environment variable should be substituted
    assert hasattr(mod, "data")
    assert mod.data == "value_from_env"
    # Clean up
    del os.environ["TEST_ENV"]


def test_load_module_missing_env_var_raises(tmp_path):
    # Ensure the env var is not set
    os.environ.pop("MISSING_ENV", None)
    cfg_file = tmp_path / "bad.cfg"
    cfg_file.write_text("value = '${MISSING_ENV}'\n")
    # Loading should raise LoadFileException
    with pytest.raises(LoadFileException) as excinfo:
        load_module_from_file_location(str(cfg_file))
    assert "MISSING_ENV" in str(excinfo.value)
