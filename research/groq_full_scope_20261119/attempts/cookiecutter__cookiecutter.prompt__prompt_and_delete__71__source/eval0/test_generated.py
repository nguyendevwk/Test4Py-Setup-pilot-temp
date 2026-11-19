import os
import sys
import pytest
from pathlib import Path

from cookiecutter.prompt import prompt_and_delete


def test_prompt_and_delete_removes_file(tmp_path):
    """When no_input is True, a file is deleted and True is returned."""
    file_path = tmp_path / "old.zip"
    file_path.write_text("old content")
    assert file_path.exists()

    result = prompt_and_delete(file_path, no_input=True)
    assert result is True
    assert not file_path.exists()


def test_prompt_and_delete_removes_directory(tmp_path):
    """When no_input is True, a directory is removed and True is returned."""
    dir_path = tmp_path / "old_dir"
    dir_path.mkdir()
    (dir_path / "subfile.txt").write_text("subcontent")
    assert dir_path.exists() and dir_path.is_dir()

    result = prompt_and_delete(dir_path, no_input=True)
    assert result is True
    assert not dir_path.exists()


def test_prompt_and_delete_nonexistent_path_raises(tmp_path):
    """If the path does not exist, os.remove or rmtree raises FileNotFoundError."""
    nonexistent = tmp_path / "does_not_exist"
    assert not nonexistent.exists()

    with pytest.raises(FileNotFoundError):
        prompt_and_delete(nonexistent, no_input=True)
