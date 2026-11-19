import os
import sys
import tempfile
import pytest
from pathlib import Path
from flutils.pathutils import normalize_path

def test_normalize_with_home_and_env(tmp_path: Path, monkeypatch):
    # Setup environment variable and home directory
    monkeypatch.setenv("TEST_VAR", "value")
    user_home = tmp_path / "home_user"
    user_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: user_home)

    # Create a path that uses ~ and an env var
    raw_path = "~/folder/${TEST_VAR}/file.txt"
    # Normalize
    result = normalize_path(raw_path)

    # Expected path: home_user/folder/value/file.txt
    expected = user_home / "folder" / "value" / "file.txt"
    assert result == expected
    assert isinstance(result, Path)

def test_normalize_relative_path(tmp_path: Path, monkeypatch):
    # Change current working directory to a known location
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)

    # Relative path with redundant separators and up-level references
    raw_path = "subdir//file.txt/../another.txt"
    result = normalize_path(raw_path)

    # Expected: cwd/subdir/another.txt
    expected = cwd / "subdir" / "another.txt"
    assert result == expected
    assert isinstance(result, Path)

def test_normalize_bytes_input(tmp_path: Path, monkeypatch):
    # Create a file in a temporary directory
    file_path = tmp_path / "sample.txt"
    file_path.write_text("content")

    # Use bytes input
    raw_bytes = str(file_path).encode(sys.getfilesystemencoding())
    result = normalize_path(raw_bytes)

    # Result should be the same Path object as file_path
    assert result == file_path
    assert isinstance(result, Path)
