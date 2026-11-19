import os
import pytest
from thefuck.rules.cat_dir import match

class DummyCommand:
    def __init__(self, output, script_parts):
        self.output = output
        self.script_parts = script_parts

def test_match_detects_cat_dir(tmp_path):
    # Create a temporary directory to act as the target
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    cmd = DummyCommand(
        output="cat: somefile.txt: No such file or directory",
        script_parts=["cat", str(dir_path)]
    )
    assert match(cmd) is True

def test_match_fails_when_output_not_starting_with_cat():
    cmd = DummyCommand(
        output="ls: cannot access 'nonexistent': No such file or directory",
        script_parts=["cat", "/tmp"]
    )
    assert match(cmd) is False

def test_match_raises_index_error_when_script_parts_too_short():
    cmd = DummyCommand(
        output="cat: /tmp: No such file or directory",
        script_parts=["cat"]  # missing second part
    )
    with pytest.raises(IndexError):
        match(cmd)
