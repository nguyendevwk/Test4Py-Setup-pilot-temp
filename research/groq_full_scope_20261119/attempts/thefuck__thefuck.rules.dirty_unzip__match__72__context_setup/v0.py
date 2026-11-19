import os
import zipfile
import pytest
from thefuck.rules.dirty_unzip import match

class DummyCommand:
    def __init__(self, script: str):
        self.script = script
        self.script_parts = script.split()

def create_zip(path, names):
    with zipfile.ZipFile(path, 'w') as z:
        for name in names:
            z.writestr(name, b"content")

def test_match_returns_true_for_bad_zip(tmp_path):
    # Create a zip with two files
    zip_path = tmp_path / "archive.zip"
    create_zip(zip_path, ["file1.txt", "file2.txt"])
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is True

def test_match_returns_false_for_good_zip_and_no_d_flag(tmp_path):
    # Create a zip with a single file
    zip_path = tmp_path / "single.zip"
    create_zip(zip_path, ["only.txt"])
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is False

def test_match_returns_false_for_invalid_zip_and_d_flag(tmp_path):
    # Create an invalid zip file
    bad_zip_path = tmp_path / "bad.zip"
    bad_zip_path.write_text("not a zip")
    cmd = DummyCommand(f"unzip -d {bad_zip_path}")
    # '-d' flag should cause immediate False
    assert match(cmd) is False
