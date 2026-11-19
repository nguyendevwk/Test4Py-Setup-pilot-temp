import os
import sys
import tty
import termios
import pytest
from thefuck.system.unix import getch

def test_getch_reads_single_character(tmp_path):
    # Create a pipe to simulate stdin
    r_fd, w_fd = os.pipe()
    try:
        # Write a single byte to the write end
        os.write(w_fd, b'x')
        # Replace sys.stdin with a file object from the read end
        sys.stdin = os.fdopen(r_fd, 'rb', buffering=0)
        # Call getch and verify it returns the written byte
        result = getch()
        assert result == 'x'
        # After reading, the pipe should be empty
        assert sys.stdin.read(1) == ''
    finally:
        # Restore original stdin
        sys.stdin = sys.__stdin__
        os.close(w_fd)

def test_getch_restores_terminal_attributes(tmp_path):
    # Create a pipe to simulate stdin
    r_fd, w_fd = os.pipe()
    try:
        # Write a byte to ensure getch can read
        os.write(w_fd, b'y')
        # Replace sys.stdin with a file object from the read end
        sys.stdin = os.fdopen(r_fd, 'rb', buffering=0)
        # Capture the original terminal attributes
        original_attrs = termios.tcgetattr(r_fd)
        # Call getch
        _ = getch()
        # After getch, attributes should be restored to original
        restored_attrs = termios.tcgetattr(r_fd)
        assert restored_attrs == original_attrs
    finally:
        sys.stdin = sys.__stdin__
        os.close(w_fd)

def test_getch_raises_on_non_tty_input(tmp_path):
    # Create a pipe to simulate stdin (not a tty)
    r_fd, w_fd = os.pipe()
    try:
        os.write(w_fd, b'z')
        sys.stdin = os.fdopen(r_fd, 'rb', buffering=0)
        # termios.tcgetattr on a pipe raises termios.error
        with pytest.raises(termios.error):
            getch()
    finally:
        sys.stdin = sys.__stdin__
        os.close(w_fd)
