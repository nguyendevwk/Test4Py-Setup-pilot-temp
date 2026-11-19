import os
import zipfile
import pytest
from thefuck.rules.dirty_unzip import side_effect, _zip_file


def test_removes_files_inside_cwd(tmp_path):
    # Create a file that will be removed
    target_file = tmp_path / "to_remove.txt"
    target_file.write_text("remove me")
    # Create a zip containing that file
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(target_file, arcname="to_remove.txt")
    # Run side_effect
    side_effect(f"unzip {zip_path}", None)
    # The file should be removed
    assert not target_file.exists()


def test_skips_files_outside_cwd(tmp_path):
    # Create a file outside cwd (simulated by a relative path that goes up)
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("do not remove")
    # Create a zip containing a path that would resolve outside cwd
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(outside_file, arcname="../outside.txt")
    # Run side_effect
    side_effect(f"unzip {zip_path}", None)
    # The outside file should still exist
    assert outside_file.exists()


def test_handles_directory_entries(tmp_path):
    # Create a directory and a file inside it
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    file_in_dir = dir_path / "file.txt"
    file_in_dir.write_text("content")
    # Create a zip containing the directory entry and the file
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.write(dir_path, arcname="dir/")
        z.write(file_in_dir, arcname="dir/file.txt")
    # Run side_effect; it should not raise an exception for the directory entry
    side_effect(f"unzip {zip_path}", None)
    # The file inside the directory should be removed
    assert not file_in_dir.exists()
    # The directory itself should still exist (os.remove does not delete directories)
    assert dir_path.exists()
