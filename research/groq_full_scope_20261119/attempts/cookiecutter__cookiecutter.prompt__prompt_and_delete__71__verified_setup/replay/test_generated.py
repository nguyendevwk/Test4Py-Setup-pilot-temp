import os
import sys
import pytest
from pathlib import Path
from cookiecutter.prompt import prompt_and_delete, read_user_yes_no

def test_prompt_and_delete_no_input_deletes_file(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")
    # Ensure file exists
    assert file_path.exists()
    # Call with no_input=True, should delete the file
    result = prompt_and_delete(file_path, no_input=True)
    assert result is True
    assert not file_path.exists()

def test_prompt_and_delete_user_allows_delete(tmp_path, monkeypatch):
    # Create a temporary directory
    dir_path = tmp_path / "temp_dir"
    dir_path.mkdir()
    # Ensure directory exists
    assert dir_path.is_dir()
    # Mock read_user_yes_no to return True for deletion prompt
    monkeypatch.setattr("cookiecutter.prompt.read_user_yes_no", lambda q, d: True)
    # Call function, should delete the directory
    result = prompt_and_delete(dir_path)
    assert result is True
    assert not dir_path.exists()

def test_prompt_and_delete_user_reuse_and_exit(tmp_path, monkeypatch):
    # Create a temporary file
    file_path = tmp_path / "temp.txt"
    file_path.write_text("content")
    # Mock read_user_yes_no to simulate user saying no to delete, then no to reuse
    responses = iter([False, False])
    monkeypatch.setattr("cookiecutter.prompt.read_user_yes_no", lambda q, d: next(responses))
    # Mock sys.exit to raise SystemExit
    monkeypatch.setattr(sys, "exit", lambda: (_ for _ in ()).throw(SystemExit))
    # Expect SystemExit when user chooses not to reuse
    with pytest.raises(SystemExit):
        prompt_and_delete(file_path)
    # File should still exist
    assert file_path.exists()
