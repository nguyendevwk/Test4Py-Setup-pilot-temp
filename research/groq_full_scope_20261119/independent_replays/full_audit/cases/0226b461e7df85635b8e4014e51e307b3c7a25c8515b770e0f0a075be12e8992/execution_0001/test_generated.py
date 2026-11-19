import os
import sys
import io
import tty
import termios
import pytest
from thefuck.system.unix import getch

# Helper to replace termios and tty functions with no-ops
def noop(*args, **kwargs):
    return None

@pytest.fixture
def patched_termios(monkeypatch):
    monkeypatch.setattr(termios, "tcgetattr", lambda fd: [0] * 19)
    monkeypatch.setattr(termios, "tcsetattr", noop)
    monkeypatch.setattr(tty, "setraw", noop)

def test_getch_single_char(tmp_path, patched_termios):
    r_fd, w_fd = os.pipe()
    try:
        # Write a single character to the write end
        os.write(w_fd, b"a")
        # Replace sys.stdin with a file object from the read end
        sys.stdin = os.fdopen(r_fd, "r", closefd=False)
        # Call getch and verify it returns the character
        result = getch()
        assert result == "a"
    finally:
        os.close(w_fd)

def test_getch_multiple_chars(tmp_path, patched_termios):
    r_fd, w_fd = os.pipe()
    try:
        # Write multiple characters
        os.write(w_fd, b"hello")
        sys.stdin = os.fdopen(r_fd, "r", closefd=False)
        # First call should return 'h'
        assert getch() == "h"
        # Subsequent calls return next characters
        assert getch() == "e"
        assert getch() == "l"
    finally:
        os.close(w_fd)

def test_getch_raises_on_tcgetattr_error(monkeypatch):
    # Simulate tcgetattr raising an exception
    monkeypatch.setattr(termios, "tcgetattr", lambda fd: (_ for _ in ()).throw(OSError("fail")))
    r_fd, w_fd = os.pipe()
    try:
        os.write(w_fd, b"x")
        sys.stdin = os.fdopen(r_fd, "r", closefd=False)
        with pytest.raises(OSError, match="fail"):
            getch()
    finally:
        os.close(w_fd)
