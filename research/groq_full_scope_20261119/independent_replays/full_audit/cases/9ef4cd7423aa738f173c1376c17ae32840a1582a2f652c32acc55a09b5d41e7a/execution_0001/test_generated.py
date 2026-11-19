import os
import types
import pytest
from pathlib import Path

from sanic.utils import load_module_from_file_location, LoadFileException, PyFileError


def test_load_module_from_py_file(tmp_path):
    # Create a simple Python module file
    module_path = tmp_path / "sample.py"
    module_path.write_text("x = 42\n", encoding="utf8")

    # Load the module using the utility
    mod = load_module_from_file_location(str(module_path))

    # Verify that the module is a module object and contains the expected attribute
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "x")
    assert mod.x == 42


def test_load_module_with_env_var(tmp_path):
    # Set an environment variable that will be used in the path
    os.environ["TEST_DIR"] = str(tmp_path)

    # Create a Python file in the temporary directory
    module_path = tmp_path / "env_module.py"
    module_path.write_text("value = 'env'", encoding="utf8")

    # Use the environment variable in the path string
    path_with_env = f"/{os.environ['TEST_DIR']}/env_module.py"

    # Load the module
    mod = load_module_from_file_location(path_with_env)

    # Verify that the module was loaded correctly
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "value")
    assert mod.value == "env"

    # Clean up the environment variable
    del os.environ["TEST_DIR"]


def test_load_module_missing_env_var_raises(tmp_path):
    # Ensure the environment variable is not set
    os.environ.pop("MISSING_VAR", None)

    # Create a Python file that references a missing environment variable
    module_path = tmp_path / "missing_env.py"
    module_path.write_text("x = 1\n", encoding="utf8")

    # Path containing an undefined environment variable
    bad_path = f"/{module_path.parent}/missing_${{MISSING_VAR}}.py"

    # Attempt to load the module and expect a LoadFileException
    with pytest.raises(LoadFileException) as excinfo:
        load_module_from_file_location(bad_path)

    # Verify that the exception message mentions the missing variable
    assert "MISSING_VAR" in str(excinfo.value)
