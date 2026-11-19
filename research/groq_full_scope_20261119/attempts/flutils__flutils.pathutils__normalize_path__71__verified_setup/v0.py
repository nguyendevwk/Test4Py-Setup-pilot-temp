import os
import sys
import tempfile
import pytest
from flutils.pathutils import normalize_path
from pathlib import Path

def test_normalize_absolute_and_relative(tmp_path):
    # Create a nested directory structure
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    # Relative path with redundant separators and up-level references
    rel_path = os.path.join("a", "b", "c", "..", "d")
    # Normalize and check that the result is absolute and correct
    result = normalize_path(rel_path)
    expected = tmp_path / "a" / "b" / "d"
    assert result == expected
    assert result.is_absolute()
    # Ensure that the returned object is a new Path instance
    assert result is not nested

def test_normalize_with_user_and_env(tmp_path, monkeypatch):
    # Set a fake home directory for the current user
    fake_home = tmp_path / "home_user"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    # Create a file in the fake home directory
    file_in_home = fake_home / "file.txt"
    file_in_home.touch()
    # Set an environment variable that points to the file
    monkeypatch.setenv("MYFILE", str(file_in_home))
    # Path containing ~ and an env variable
    path_with_vars = "~/file.txt:$MYFILE"
    # Normalize and verify that both ~ and $MYFILE are expanded correctly
    result = normalize_path(path_with_vars)
    # The result should be the absolute path to the file in the fake home
    expected = fake_home / "file.txt"
    assert result == expected
    # Ensure that the environment variable part was ignored after expansion
    assert "$MYFILE" not in str(result)

def test_normalize_bytes_input(tmp_path):
    # Create a file to normalize
    file_path = tmp_path / "data.bin"
    file_path.write_bytes(b"content")
    # Encode the path as bytes using the filesystem encoding
    bytes_path = file_path.as_posix().encode(sys.getfilesystemencoding())
    # Normalize the bytes path and check that it matches the Path object
    result = normalize_path(bytes_path)
    assert result == file_path
    assert isinstance(result, Path)
