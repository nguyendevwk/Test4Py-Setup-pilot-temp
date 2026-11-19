import os
import sys
import pytest
from pathlib import Path
from cookiecutter.prompt import prompt_and_delete


def test_prompt_and_delete_removes_existing_file(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "testfile.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Call the function with no_input=True to force deletion
    result = prompt_and_delete(file_path, no_input=True)

    # The function should return True and the file should be removed
    assert result is True
    assert not file_path.exists()


def test_prompt_and_delete_removes_existing_directory(tmp_path):
    # Create a temporary directory with a file inside
    dir_path = tmp_path / "testdir"
    dir_path.mkdir()
    (dir_path / "inner.txt").write_text("inner")
    assert dir_path.exists()
    assert (dir_path / "inner.txt").exists()

    # Call the function with no_input=True to force deletion
    result = prompt_and_delete(dir_path, no_input=True)

    # The function should return True and the directory should be removed
    assert result is True
    assert not dir_path.exists()


def test_prompt_and_delete_raises_when_path_missing(tmp_path):
    # Define a path that does not exist
    missing_path = tmp_path / "nonexistent.txt"
    assert not missing_path.exists()

    # Calling with no_input=True should attempt to delete and raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        prompt_and_delete(missing_path, no_input=True)
