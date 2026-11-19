import os
import sys
import pytest
from pathlib import Path
from flutils.pathutils import normalize_path

def test_normalize_absolute_path(tmp_path):
    # Create a nested directory structure
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    # Path with redundant separators and up-level references
    raw = str(nested) + "/../d/./e"
    expected = Path(tmp_path) / "a" / "b" / "d" / "e"
    result = normalize_path(raw)
    assert result == expected
    assert isinstance(result, Path)

def test_normalize_with_env_and_user(tmp_path, monkeypatch):
    # Set an environment variable and a fake home directory
    monkeypatch.setenv("TEST_VAR", "folder")
    fake_home = tmp_path / "home_user"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    # Path using ~ and env var
    raw = "~/subdir/$TEST_VAR/file.txt"
    expected = fake_home / "subdir" / "folder" / "file.txt"
    result = normalize_path(raw)
    assert result == expected
    assert isinstance(result, Path)

def test_normalize_bytes_and_relative(tmp_path):
    # Create a relative path that is not absolute
    rel = Path("relative") / "path"
    rel.mkdir(parents=True)
    # Convert to bytes using filesystem encoding
    raw_bytes = rel.as_posix().encode(sys.getfilesystemencoding())
    # Normalize should prepend cwd and return a Path
    result = normalize_path(raw_bytes)
    expected = Path(os.getcwd()) / rel
    assert result == expected
    assert isinstance(result, Path)
