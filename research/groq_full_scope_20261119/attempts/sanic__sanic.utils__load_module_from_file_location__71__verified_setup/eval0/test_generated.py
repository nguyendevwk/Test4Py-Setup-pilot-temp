import os
import types
import pytest
from pathlib import Path
from sanic.utils import load_module_from_file_location, LoadFileException, PyFileError

def test_load_python_file(tmp_path):
    # Create a simple python file
    py_file = tmp_path / "sample.py"
    py_file.write_text("x = 42\n")
    mod = load_module_from_file_location(str(py_file))
    assert isinstance(mod, types.ModuleType)
    assert hasattr(mod, "x")
    assert mod.x == 42

def test_env_var_substitution_error(tmp_path):
    # File path contains an undefined environment variable
    env_path = tmp_path / "config_${UNSET_VAR}.py"
    env_path.write_text("y = 10\n")
    with pytest.raises(LoadFileException) as exc:
        load_module_from_file_location(str(env_path))
    assert "UNSET_VAR" in str(exc.value)

def test_non_py_file_exec_error(tmp_path):
    # Create a non-py config file with invalid syntax
    cfg_file = tmp_path / "bad.cfg"
    cfg_file.write_text("invalid python code\n")
    with pytest.raises(PyFileError) as exc:
        load_module_from_file_location(str(cfg_file))
    assert str(cfg_file) in str(exc.value)
