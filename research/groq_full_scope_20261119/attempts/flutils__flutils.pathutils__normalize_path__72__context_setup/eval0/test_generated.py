import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import normalize_path

def test_normalize_absolute_and_relative(tmp_path):
    # Create a nested directory structure
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    # Absolute path should be returned unchanged (except normcase)
    abs_path = normalize_path(str(nested))
    assert isinstance(abs_path, Path)
    assert abs_path == Path(str(nested))
    # Relative path should be resolved against cwd
    os.chdir(tmp_path)
    rel_path = normalize_path("a/b/c")
    assert rel_path == Path(tmp_path) / "a/b/c"

def test_expand_user_and_env_vars(tmp_path):
    # Set up a fake home directory and environment variable
    fake_home = tmp_path / "home_user"
    fake_home.mkdir()
    os.environ["TEST_VAR"] = str(tmp_path / "var_dir")
    # Use tilde and env var in path
    path_str = "~/subdir/${TEST_VAR}/file.txt"
    # normalize_path should expand ~ and env var, then normalize
    result = normalize_path(path_str)
    expected = Path(fake_home) / "subdir" / os.environ["TEST_VAR"] / "file.txt"
    # normpath removes any redundant separators
    assert result == expected

def test_bytes_input_and_case_normalization(tmp_path):
    # Create a file with mixed case
    mixed_case = tmp_path / "MiXeD" / "PaTh"
    mixed_case.mkdir(parents=True)
    # Path as bytes
    path_bytes = bytes(str(mixed_case), sys.getfilesystemencoding())
    result = normalize_path(path_bytes)
    # On Windows, normcase lowercases; on POSIX, it is identity
    if os.name == "nt":
        expected = Path(str(mixed_case).lower())
    else:
        expected = Path(str(mixed_case))
    assert result == expected
