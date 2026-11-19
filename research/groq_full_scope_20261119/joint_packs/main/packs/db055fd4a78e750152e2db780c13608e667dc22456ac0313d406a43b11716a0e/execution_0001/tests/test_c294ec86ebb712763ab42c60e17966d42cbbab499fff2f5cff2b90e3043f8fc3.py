import os
import sys
import builtins
import types
import pytest
from pathlib import Path

# Import the target function and its module
from cookiecutter.prompt import prompt_and_delete, read_user_yes_no


def test_no_input_deletes_file(tmp_path):
    """When no_input is True, the function should delete the file and return True."""
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")

    # Ensure the file exists before calling
    assert file_path.exists()

    # Call the function with no_input=True
    result = prompt_and_delete(file_path, no_input=True)

    # The function should return True and the file should be removed
    assert result is True
    assert not file_path.exists()


def test_reuse_returns_false(tmp_path, monkeypatch):
    """When the user declines deletion but accepts reuse, the function should return False."""
    # Create a temporary directory
    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()

    # Ensure the directory exists before calling
    assert dir_path.exists()

    # Patch read_user_yes_no to simulate user responses:
    # first call (delete prompt) returns False, second call (reuse prompt) returns True
    responses = iter([False, True])
    monkeypatch.setattr(
        "cookiecutter.prompt.read_user_yes_no",
        lambda *args, **kwargs: next(responses),
    )

    # Call the function with no_input=False (default)
    result = prompt_and_delete(dir_path, no_input=False)

    # The function should return False and the directory should remain
    assert result is False
    assert dir_path.exists()


def test_exit_on_no_reuse(tmp_path, monkeypatch):
    """When the user declines both deletion and reuse, the function should exit."""
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")

    # Ensure the file exists before calling
    assert file_path.exists()

    # Patch read_user_yes_no to simulate user responses:
    # first call (delete prompt) returns False, second call (reuse prompt) returns False
    responses = iter([False, False])
    monkeypatch.setattr(
        "cookiecutter.prompt.read_user_yes_no",
        lambda *args, **kwargs: next(responses),
    )

    # The function should raise SystemExit
    with pytest.raises(SystemExit):
        prompt_and_delete(file_path, no_input=False)

    # The file should still exist after the exit
    assert file_path.exists()
