import io
import sys
import pytest
from tornado.options import print_help, options

def test_print_help_default_output(capsys):
    # print_help should write to stderr by default
    print_help()
    captured = capsys.readouterr()
    # stderr should contain the option list header
    assert "Options:" in captured.err
    # stdout should be empty
    assert captured.out == ""

def test_print_help_to_file(tmp_path):
    # print_help should write to a provided file object
    file_path = tmp_path / "help.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        print_help(f)
    # Verify file contents
    content = file_path.read_text(encoding="utf-8")
    assert "Options:" in content
    # Ensure no output to stderr
    # (cannot capture here, but file content suffices)

def test_print_help_returns_none():
    # The function should return None explicitly
    result = print_help()
    assert result is None
