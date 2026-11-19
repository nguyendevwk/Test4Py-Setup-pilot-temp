import os
import zipfile
import pytest
from thefuck.rules.dirty_unzip import match

class DummyCommand:
    def __init__(self, script):
        self.script = script
        self.script_parts = script.split()

def test_match_single_file_zip(tmp_path):
    # Create a zip file with a single entry
    zip_path = tmp_path / "single.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("file.txt", "content")
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is False

def test_match_multiple_files_zip(tmp_path):
    # Create a zip file with multiple entries
    zip_path = tmp_path / "multi.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("file1.txt", "content1")
        z.writestr("file2.txt", "content2")
    cmd = DummyCommand(f"unzip {zip_path}")
    assert match(cmd) is True

def test_match_no_zip_or_flag(tmp_path):
    # No zip file in command and '-d' flag present
    zip_path = tmp_path / "single.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("file.txt", "content")
    cmd_no_zip = DummyCommand(f"unzip -d {zip_path}")
    assert match(cmd_no_zip) is False
    cmd_no_zip2 = DummyCommand(f"unzip {zip_path} -d")
    assert match(cmd_no_zip2) is False
    cmd_no_zip3 = DummyCommand(f"unzip {zip_path} -x")
    assert match(cmd_no_zip3) is False
