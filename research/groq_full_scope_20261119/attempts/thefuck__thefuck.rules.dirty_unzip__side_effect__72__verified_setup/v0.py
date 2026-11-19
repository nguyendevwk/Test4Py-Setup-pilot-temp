import os
import zipfile
import pytest
from thefuck.rules.dirty_unzip import side_effect

def create_zip_with_entries(zip_path, entries):
    """Helper to create a zip file with specified entries."""
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for entry in entries:
            # For file entries, write empty content
            if not entry.endswith('/'):
                zf.writestr(entry, b'')
            else:
                # Directory entries are added as empty entries
                zf.writestr(entry, b'')

def test_side_effect_removes_safe_files(tmp_path):
    # Setup: create a file in the current working directory
    cwd_file = tmp_path / "keep.txt"
    cwd_file.write_text("keep")
    # Create a zip containing that file and an outside file
    zip_path = tmp_path / "test.zip"
    create_zip_with_entries(zip_path, ["keep.txt", "/tmp/outside.txt"])
    # Run side_effect
    result = side_effect("unzip test.zip", f"unzip {zip_path}")
    # Assertions
    assert result is None
    assert not cwd_file.exists()  # file should be removed
    # Outside file should not exist in cwd and should not be removed
    outside_path = Path("/tmp/outside.txt")
    assert not outside_path.exists()

def test_side_effect_skips_outside_files(tmp_path):
    # Create a zip with an absolute path that is outside cwd
    zip_path = tmp_path / "outside.zip"
    create_zip_with_entries(zip_path, ["/etc/passwd"])
    # Ensure the file does not exist in cwd
    outside_in_cwd = tmp_path / "etc" / "passwd"
    assert not outside_in_cwd.exists()
    # Run side_effect
    side_effect("unzip outside.zip", f"unzip {zip_path}")
    # No exception should be raised and nothing should be removed
    assert not outside_in_cwd.exists()

def test_side_effect_handles_directory_entries(tmp_path):
    # Create a zip with a directory entry
    zip_path = tmp_path / "dir.zip"
    create_zip_with_entries(zip_path, ["folder/"])
    # Run side_effect; it should not raise an exception for directory entries
    side_effect("unzip dir.zip", f"unzip {zip_path}")
    # No files were created, so nothing to assert beyond no exception
    assert True
