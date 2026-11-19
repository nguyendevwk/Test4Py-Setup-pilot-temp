import os
import sys
import tty
import termios
import pytest
from thefuck.system.unix import getch

def _pipe_with_data(data: bytes):
    """Create a pipe and write data to the write end."""
    r, w = os.pipe()
    os.write(w, data)
    os.close(w)
    return r

def test_getch_reads_single_character(tmp_path):
    """getch should return the first character from stdin."""
    r_fd = _pipe_with_data(b"abc")
    # Replace sys.stdin with the read end of the pipe
    sys.stdin = os.fdopen(r_fd, "r")
    try:
        first = getch()
        second = getch()
    finally:
        sys.stdin.close()
    assert first == "a"
    assert second == "b"

def test_getch_restores_terminal_attributes(tmp_path):
    """getch should restore terminal attributes even if an exception occurs."""
    r_fd = _pipe_with_data(b"x")
    sys.stdin = os.fdopen(r_fd, "r")
    old_attrs = termios.tcgetattr(sys.stdin.fileno())
    try:
        # Force an exception by closing the file descriptor before reading
        sys.stdin.close()
        with pytest.raises(Exception):
            getch()
    finally:
        # After getch, terminal attributes should be restored to old_attrs
        # We cannot read from stdin now, but we can check that the attributes
        # of the original file descriptor (r_fd) match old_attrs
        restored_attrs = termios.tcgetattr(r_fd)
        assert restored_attrs == old_attrs

def test_getch_raises_on_non_tty(tmp_path):
    """getch should raise a termios.error when stdin is not a tty."""
    r_fd = _pipe_with_data(b"y")
    # Use a regular file (not a tty) as stdin
    sys.stdin = os.fdopen(r_fd, "r")
    try:
        with pytest.raises(termios.error):
            getch()
    finally:
        sys.stdin.close()
