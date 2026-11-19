import os
import zipfile
import pytest
from pathlib import Path

# Import the side_effect function from the target module
from thefuck.rules.dirty_unzip import side_effect


def create_zip_with_entries(zip_path, entries):
    """Helper to create a zip file with given entries."""
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for entry_name, content in entries.items():
            # Ensure the entry is added as a file (not a directory)
            zf.writestr(entry_name, content)


def test_removal_of_safe_files(tmp_path):
    """Files inside the current working directory should be removed."""
    # Setup: create a file that will be removed
    target_file = tmp_path / "remove_me.txt"
    target_file.write_text("to be removed")

    # Create a zip containing that file
    zip_path = tmp_path / "archive.zip"
    create_zip_with_entries(zip_path, {"remove_me.txt": "content"})

    # Run side_effect
    old_cmd = f"unzip {zip_path}"
    side_effect(old_cmd, None)

    # Assert the file has been removed
    assert not target_file.exists()


def test_skip_unsafe_files(tmp_path, monkeypatch):
    """Files outside the current working directory should not be removed."""
    # Create a file outside cwd
    outside_file = Path(tmp_path.parent) / "outside.txt"
    outside_file.write_text("outside content")

    # Create a zip containing a relative path that points outside
    zip_path = tmp_path / "archive.zip"
    create_zip_with_entries(zip_path, {"../outside.txt": "content"})

    # Run side_effect
    old_cmd = f"unzip {zip_path}"
    side_effect(old_cmd, None)

    # The outside file should still exist
    assert outside_file.exists()


def test_ignore_oserror_on_directory(tmp_path):
    """If os.remove raises OSError (e.g., for directories), it should be ignored."""
    # Create a directory that will be listed in the zip
    dir_path = tmp_path / "dir_to_keep"
    dir_path.mkdir()
    # Create a zip containing a directory entry
    zip_path = tmp_path / "archive.zip"
    create_zip_with_entries(zip_path, {"dir_to_keep/": ""})  # empty content for dir

    # Run side_effect; should not raise
    old_cmd = f"unzip {zip_path}"
    side_effect(old_cmd, None)

    # Directory should still exist
    assert dir_path.is_dir()
