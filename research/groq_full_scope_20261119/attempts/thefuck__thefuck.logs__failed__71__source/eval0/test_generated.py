import sys
import io
import pytest
from thefuck.logs import failed
from colorama import Fore, Style

def test_failed_writes_colored_message(capsys):
    """The failed function should write the message wrapped in red color codes."""
    msg = "Error occurred"
    failed(msg)
    captured = capsys.readouterr()
    # The output should contain the red color code, the message, and the reset code
    assert Fore.RED in captured.err
    assert Style.RESET_ALL in captured.err
    assert msg in captured.err
    # Ensure a newline is appended
    assert captured.err.endswith('\n')

def test_failed_handles_empty_message(capsys):
    """An empty message should still produce a newline with reset codes."""
    failed("")
    captured = capsys.readouterr()
    # Should contain only the reset code and a newline
    assert captured.err.strip() == Style.RESET_ALL
    assert captured.err.endswith('\n')

def test_failed_does_not_raise_on_unicode(capsys):
    """The function should handle Unicode characters without raising."""
    msg = "Unicode test: 測試"
    failed(msg)
    captured = capsys.readouterr()
    assert msg in captured.err
    assert Fore.RED in captured.err
    assert Style.RESET_ALL in captured.err
