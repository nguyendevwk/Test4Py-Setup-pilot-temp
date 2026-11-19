import os
import pytest
from thefuck.rules.cat_dir import match


class DummyCommand:
    def __init__(self, output, script_parts):
        self.output = output
        self.script_parts = script_parts


def test_match_true(tmp_path):
    """When output starts with 'cat: ' and the second script part is a directory, match returns True."""
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    cmd = DummyCommand(output="cat: something", script_parts=["cat", str(dir_path)])
    assert match(cmd) is True


def test_match_false_when_not_dir(tmp_path):
    """When output starts with 'cat: ' but the second script part is not a directory, match returns False."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")
    cmd = DummyCommand(output="cat: something", script_parts=["cat", str(file_path)])
    assert match(cmd) is False


def test_match_raises_index_error_when_missing_script_part():
    """When script_parts has fewer than two elements, accessing index 1 raises IndexError."""
    cmd = DummyCommand(output="cat: something", script_parts=["cat"])
    with pytest.raises(IndexError):
        match(cmd)
