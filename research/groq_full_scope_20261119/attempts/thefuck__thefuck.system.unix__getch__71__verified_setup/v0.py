import os
import sys
import subprocess
import pty
import tempfile
import pytest
from thefuck.system.unix import getch

def _run_getch_with_input(input_bytes: bytes) -> str:
    """Run a subprocess that imports getch and prints the returned character."""
    script = (
        "import sys\n"
        "from thefuck.system.unix import getch\n"
        "print(getch(), end='')\n"
    )
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            [sys.executable, "-c", script],
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        os.write(master, input_bytes)
        out, _ = proc.communicate(timeout=1)
        return out.decode()
    finally:
        os.close(master)
        os.close(slave)

def test_getch_returns_first_character():
    """getch should return the first character from stdin."""
    result = _run_getch_with_input(b"ab")
    assert result == "a", f"Expected 'a', got {result!r}"

def test_getch_reads_single_character_even_if_more_available():
    """getch reads only one character even if more are present."""
    result = _run_getch_with_input(b"xyz")
    assert result == "x", f"Expected 'x', got {result!r}"

def test_getch_raises_on_non_tty_input(tmp_path):
    """getch should raise an exception when stdin is not a tty."""
    tmp_file = tmp_path / "input.txt"
    tmp_file.write_text("test")
    with open(tmp_file, "rb") as f:
        with pytest.raises((OSError, ValueError)):
            # Redirect sys.stdin to a file descriptor that is not a tty
            old_stdin = sys.stdin
            sys.stdin = f
            try:
                getch()
            finally:
                sys.stdin = old_stdin
