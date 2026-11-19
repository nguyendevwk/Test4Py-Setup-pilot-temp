import os
import zipfile
import tempfile
import shutil
import pytest
from pathlib import Path

# Import the target function and helper
from thefuck.rules.dirty_unzip import side_effect, _zip_file


class DummyCommand:
    """Simple stand‑in for the command object used by thefuck."""
    def __init__(self, script_parts):
        self.script_parts = script_parts


def create_zip(zip_path, files):
    """Create a zip file containing the given file paths."""
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file_path in files:
            zf.write(file_path, arcname=file_path.name)


def test_side_effect_removes_files_within_cwd(tmp_path):
    """Files listed in the zip that are inside the current working directory
    should be removed by side_effect."""
    # Set up a file inside cwd
    cwd_file = tmp_path / "inside.txt"
    cwd_file.write_text("content")
    # Create a zip containing that file
    zip_path = tmp_path / "archive.zip"
    create_zip(zip_path, [cwd_file])

    # Run side_effect
    cmd = DummyCommand(["unzip", str(zip_path)])
    side_effect(cmd, None)

    # Assert the file has been removed
    assert not cwd_file.exists()


def test_side_effect_skips_files_outside_cwd(tmp_path):
    """Files listed in the zip that are outside the current working directory
    should not be removed by side_effect."""
    # Create a parent directory and a file there
    parent_dir = tmp_path.parent
    outside_file = parent_dir / "outside.txt"
    outside_file.write_text("outside")
    # Create a zip containing that file
    zip_path = tmp_path / "archive.zip"
    create_zip(zip_path, [outside_file])

    # Run side_effect
    cmd = DummyCommand(["unzip", str(zip_path)])
    side_effect(cmd, None)

    # Assert the outside file still exists
    assert outside_file.exists()


def test_side_effect_handles_directory_entries(tmp_path):
    """If the zip contains a directory entry, side_effect should not raise an exception."""
    # Create a directory inside cwd
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    # Create a zip containing the directory entry
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(dir_path, arcname=dir_path.name + "/")  # directory entry

    # Run side_effect and ensure no exception is raised
    cmd = DummyCommand(["unzip", str(zip_path)])
    try:
        side_effect(cmd, None)
    except Exception as exc:
        pytest.fail(f"side_effect raised an exception with a directory entry: {exc}")
