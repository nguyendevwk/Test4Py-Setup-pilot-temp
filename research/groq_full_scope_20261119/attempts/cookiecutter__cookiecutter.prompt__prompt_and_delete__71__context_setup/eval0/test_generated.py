import os
import sys
import builtins
import importlib
import types
import pytest
from pathlib import Path

# Import the target module
import cookiecutter.prompt as prompt_module

def test_prompt_and_delete_no_input_file(tmp_path):
    """When no_input=True and path is a file, the file is removed and True is returned."""
    # Create a temporary file
    temp_file = tmp_path / "temp.zip"
    temp_file.write_text("dummy")
    assert temp_file.exists()

    # Call the function with no_input=True
    result = prompt_module.prompt_and_delete(temp_file, no_input=True)

    # Verify the file was deleted and the return value is True
    assert result is True
    assert not temp_file.exists()


def test_prompt_and_delete_no_input_dir(tmp_path):
    """When no_input=True and path is a directory, the directory is removed and True is returned."""
    # Create a temporary directory with a file inside
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()
    (temp_dir / "file.txt").write_text("content")
    assert temp_dir.exists()
    assert (temp_dir / "file.txt").exists()

    # Call the function with no_input=True
    result = prompt_module.prompt_and_delete(temp_dir, no_input=True)

    # Verify the directory was removed and the return value is True
    assert result is True
    assert not temp_dir.exists()


def test_prompt_and_delete_exit_on_user_decline(monkeypatch):
    """When the user declines both prompts, the function exits the process."""
    # Monkeypatch read_user_yes_no to simulate user declining both prompts
    def fake_read_user_yes_no(var_name, default_value, prompts=None, prefix: str = ""):
        return False

    monkeypatch.setattr(prompt_module, "read_user_yes_no", fake_read_user_yes_no)

    # Create a temporary file to pass as path
    temp_file = Path("dummy_path")
    # Ensure the file does not exist to avoid actual deletion
    if temp_file.exists():
        temp_file.unlink()

    # Expect SystemExit when both prompts return False
    with pytest.raises(SystemExit):
        prompt_module.prompt_and_delete(temp_file, no_input=False)
