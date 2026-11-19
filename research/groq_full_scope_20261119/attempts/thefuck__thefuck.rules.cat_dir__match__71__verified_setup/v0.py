import os
import pytest
from thefuck.rules.cat_dir import match

class DummyCommand:
    def __init__(self, output, script_parts):
        self.output = output
        self.script_parts = script_parts

def test_match_true(tmp_path):
    # Create a temporary directory to act as the target
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    cmd = DummyCommand(output="cat: some error", script_parts=["cat", str(dir_path)])
    assert match(cmd) is True

def test_match_false_no_dir(tmp_path):
    # Use a file instead of a directory
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    cmd = DummyCommand(output="cat: some error", script_parts=["cat", str(file_path)])
    assert match(cmd) is False

def test_match_index_error():
    # script_parts has only one element, accessing index 1 raises IndexError
    cmd = DummyCommand(output="cat: some error", script_parts=["cat"])
    with pytest.raises(IndexError):
        match(cmd)
