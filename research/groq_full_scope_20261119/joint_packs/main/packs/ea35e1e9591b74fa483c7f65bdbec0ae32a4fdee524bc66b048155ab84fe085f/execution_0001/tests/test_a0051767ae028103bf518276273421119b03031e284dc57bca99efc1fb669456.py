import os
import sys
import builtins
import pytest
from pathlib import Path
from cookiecutter.prompt import prompt_and_delete, read_user_yes_no, YesNoPrompt

# Helper to patch read_user_yes_no
def _patch_read_user_yes_no(monkeypatch, return_values):
    """Return values sequentially from the provided list."""
    iterator = iter(return_values)

    def fake_read_user_yes_no(var_name, default_value, prompts=None, prefix: str = ""):
        return next(iterator)

    monkeypatch.setattr("cookiecutter.prompt.read_user_yes_no", fake_read_user_yes_no)

def test_prompt_and_delete_no_input_deletes_file(tmp_path, monkeypatch):
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Ensure no_input forces deletion
    result = prompt_and_delete(file_path, no_input=True)
    assert result is True
    assert not file_path.exists()

def test_prompt_and_delete_user_declines_and_reuses(tmp_path, monkeypatch):
    # Create a temporary directory
    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()
    assert dir_path.is_dir()

    # Simulate user answering 'no' to delete, then 'yes' to reuse
    _patch_read_user_yes_no(monkeypatch, [False, True])

    result = prompt_and_delete(dir_path, no_input=False)
    assert result is False
    assert dir_path.is_dir()  # directory still exists

def test_prompt_and_delete_user_declines_and_exits(tmp_path, monkeypatch):
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")
    assert file_path.exists()

    # Simulate user answering 'no' to delete, then 'no' to reuse
    _patch_read_user_yes_no(monkeypatch, [False, False])

    with pytest.raises(SystemExit):
        prompt_and_delete(file_path, no_input=False)
    assert file_path.exists()
