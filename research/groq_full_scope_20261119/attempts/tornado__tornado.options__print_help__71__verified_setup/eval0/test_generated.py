import io
import sys
import tempfile
import pytest
from tornado.options import print_help, options


def test_print_help_to_stderr(capsys):
    """print_help writes the help text to stderr by default."""
    # Capture stderr
    print_help()
    captured = capsys.readouterr()
    # The output should contain the name of the module and at least one option
    assert "tornado.options" in captured.err
    assert "help" in captured.err.lower()
    # Ensure nothing was printed to stdout
    assert captured.out == ""


def test_print_help_to_file(tmp_path):
    """print_help writes the help text to a provided file object."""
    help_file = tmp_path / "help.txt"
    with help_file.open("w", encoding="utf-8") as f:
        print_help(f)
    # Verify the file contains expected content
    content = help_file.read_text(encoding="utf-8")
    assert "tornado.options" in content
    assert "help" in content.lower()


def test_print_help_returns_none():
    """print_help returns None."""
    result = print_help()
    assert result is None
