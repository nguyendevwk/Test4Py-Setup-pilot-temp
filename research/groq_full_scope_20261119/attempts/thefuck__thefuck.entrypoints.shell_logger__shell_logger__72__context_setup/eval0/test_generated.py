import os
import mmap
import array
import signal
import termios
import tty
import fcntl
import pytest
from thefuck.entrypoints.shell_logger import _read, _set_pty_size, shell_logger
from thefuck import const, logs

def test_read_wraps_when_buffer_full(tmp_path):
    """_read should wrap around when the mmap buffer is full."""
    # Create a small mmap file
    file_path = tmp_path / "log"
    fd = os.open(str(file_path), os.O_CREAT | os.O_RDWR)
    os.write(fd, b'\x00' * 10)  # small buffer
    buf = mmap.mmap(fd, 10, mmap.MAP_SHARED, mmap.PROT_WRITE)

    # Write more than buffer size to trigger ValueError
    data = b'A' * 20
    # Simulate reading from a file descriptor that returns data
    def fake_read(_fd, _n):
        return data

    # Replace os.read temporarily
    original_read = os.read
    os.read = fake_read
    try:
        _read(buf, 0)
    finally:
        os.read = original_read

    # After wrap, the buffer should contain zeros at the start
    buf.seek(0)
    assert buf.read(10) == b'\x00' * 10, "Buffer should be zeroed after wrap"

def test_shell_logger_warns_and_exits_when_no_shell(monkeypatch, caplog):
    """shell_logger should warn and exit with code 1 when SHELL env var is missing."""
    monkeypatch.delenv("SHELL", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        shell_logger("dummy_output")
    assert excinfo.value.code == 1
    assert any("Shell logger doesn't support your platform." in rec.message for rec in caplog.records)

def test_set_pty_size_does_not_raise(tmp_path):
    """_set_pty_size should not raise an exception when called with a valid fd."""
    # Use /dev/null as a dummy file descriptor
    fd = os.open("/dev/null", os.O_RDWR)
    try:
        _set_pty_size(fd)
    finally:
        os.close(fd)
