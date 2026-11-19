import io
import sys
import tempfile
import pytest
from tornado.options import print_help
from tornado import options

def test_print_help_to_stderr(capsys):
    """print_help writes the help text to stderr by default."""
    # Capture stderr
    print_help()
    captured = capsys.readouterr()
    # The output should contain the name of at least one option
    assert "help" in captured.err.lower()
    # Ensure nothing was printed to stdout
    assert captured.out == ""

def test_print_help_to_file(tmp_path):
    """print_help writes the help text to a provided file object."""
    file_path = tmp_path / "help.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        print_help(file=f)
    # Read back the file and check content
    content = file_path.read_text(encoding="utf-8")
    assert "help" in content.lower()
    # Ensure the file is not empty
    assert len(content) > 0

def test_print_help_returns_none():
    """print_help returns None explicitly."""
    result = print_help()
    assert result is None
