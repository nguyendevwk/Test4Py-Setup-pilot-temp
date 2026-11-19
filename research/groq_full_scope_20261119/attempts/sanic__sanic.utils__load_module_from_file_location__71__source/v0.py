import os
import types
import pytest
from sanic.utils import load_module_from_file_location, LoadFileException, PyFileError

def test_load_py_file(tmp_path):
    # Create a simple python file that defines a variable
    py_file = tmp_path / "sample.py"
    py_file.write_text("x = 42\n")
    module = load_module_from_file_location(str(py_file))
    assert isinstance(module, types.ModuleType)
    assert hasattr(module, "x")
    assert module.x == 42

def test_env_var_substitution(tmp_path):
    # Set an environment variable and create a file path containing it
    os.environ["TEST_ENV"] = "value"
    env_path = tmp_path / "config_${TEST_ENV}.py"
    env_path.write_text("y = 'env'\n")
    module = load_module_from_file_location(str(env_path))
    assert hasattr(module, "y")
    assert module.y == "env"
    # Clean up environment variable
    del os.environ["TEST_ENV"]

def test_missing_env_var_raises(tmp_path):
    # Path contains an undefined environment variable
    bad_path = tmp_path / "missing_${UNSET_VAR}.py"
    bad_path.write_text("z = 0\n")
    with pytest.raises(LoadFileException) as excinfo:
        load_module_from_file_location(str(bad_path))
    assert "UNSET_VAR" in str(excinfo.value)

def test_non_py_file_error(tmp_path):
    # Create a non-Python file that will raise an exception when executed
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("raise ValueError('oops')\n")
    with pytest.raises(PyFileError) as excinfo:
        load_module_from_file_location(str(bad_file))
    assert str(bad_file) in str(excinfo.value)
