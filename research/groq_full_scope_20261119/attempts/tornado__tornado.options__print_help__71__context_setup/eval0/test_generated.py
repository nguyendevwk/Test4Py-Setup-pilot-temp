import io
import os
import sys
import tempfile
import pytest
from tornado.options import print_help, options

def test_print_help_to_stderr(capsys):
    """print_help writes the help text to stderr when no file is provided."""
    # Capture stderr
    print_help()
    captured = capsys.readouterr()
    # The help text should contain the option parser name and at least one option
    assert "Options:" in captured.err
    assert "--help" in captured.err

def test_print_help_to_file(tmp_path):
    """print_help writes the help text to a file when a file object is provided."""
    # Create a temporary file
    tmp_file = tmp_path / "help.txt"
    with open(tmp_file, "w", encoding="utf-8") as f:
        print_help(f)
    # Verify the file contains the expected content
    content = tmp_file.read_text(encoding="utf-8")
    assert "Options:" in content
    assert "--help" in content

def test_print_help_returns_none():
    """print_help returns None."""
    result = print_help()
    assert result is None
