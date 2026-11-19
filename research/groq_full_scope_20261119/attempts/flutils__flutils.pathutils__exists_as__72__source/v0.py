import os
import stat
import tempfile
import pytest
from flutils.pathutils import exists_as

def test_exists_as_file(tmp_path):
    # Create a regular file
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    assert exists_as(file_path) == "file"

    # Create a symlink to the file
    link_path = tmp_path / "link.txt"
    link_path.symlink_to(file_path)
    assert exists_as(link_path) == "file"

def test_exists_as_symlink_broken(tmp_path):
    # Create a symlink pointing to a non‑existent target
    broken_link = tmp_path / "broken"
    broken_link.symlink_to(tmp_path / "does_not_exist")
    # The symlink itself exists but points to nothing
    assert exists_as(broken_link) == ""

def test_exists_as_nonexistent(tmp_path):
    # Path that does not exist at all
    missing = tmp_path / "missing"
    assert not missing.exists()
    assert exists_as(missing) == ""
