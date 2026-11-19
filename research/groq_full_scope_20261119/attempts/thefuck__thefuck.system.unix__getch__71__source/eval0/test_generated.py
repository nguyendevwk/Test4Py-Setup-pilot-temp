import io
import os
import sys
import tty
import termios
import pytest
from thefuck.system.unix import getch

# Helper to create a temporary file with a single character and reset its position
def _temp_file_with_char(char: str):
    f = os.open(os.devnull, os.O_RDWR)
    tmp = os.fdopen(f, 'w+')
    tmp.write(char)
    tmp.flush()
    tmp.seek(0)
    return tmp

def test_getch_returns_single_character(monkeypatch, tmp_path):
    # Prepare a temporary file that behaves like stdin
    tmp_file = _temp_file_with_char('x')
    monkeypatch.setattr(sys, 'stdin', tmp_file)

    # Patch tty and termios functions to avoid affecting the real terminal
    monkeypatch.setattr(tty, 'setraw', lambda fd: None)
    monkeypatch.setattr(termios, 'tcgetattr', lambda fd: [])
    monkeypatch.setattr(termios, 'tcsetattr', lambda fd, when, attrs: None)

    # Call getch and verify it returns the expected character
    result = getch()
    assert result == 'x', "getch should return the first character from stdin"

def test_getch_returns_empty_on_eof(monkeypatch):
    # Use an empty StringIO that provides a fileno via a temporary file
    tmp_file = _temp_file_with_char('')
    monkeypatch.setattr(sys, 'stdin', tmp_file)

    # Patch tty and termios functions
    monkeypatch.setattr(tty, 'setraw', lambda fd: None)
    monkeypatch.setattr(termios, 'tcgetattr', lambda fd: [])
    monkeypatch.setattr(termios, 'tcsetattr', lambda fd, when, attrs: None)

    # getch should return an empty string when EOF is reached
    result = getch()
    assert result == '', "getch should return an empty string on EOF"

def test_getch_raises_on_invalid_fileno(monkeypatch):
    # Create a dummy object that raises OSError on fileno()
    class BadStdin:
        def fileno(self):
            raise OSError("bad fileno")
        def read(self, n):
            return 'a'

    monkeypatch.setattr(sys, 'stdin', BadStdin())

    # Patch tty and termios to avoid side effects
    monkeypatch.setattr(tty, 'setraw', lambda fd: None)
    monkeypatch.setattr(termios, 'tcgetattr', lambda fd: [])
    monkeypatch.setattr(termios, 'tcsetattr', lambda fd, when, attrs: None)

    with pytest.raises(OSError, match="bad fileno"):
        getch()
