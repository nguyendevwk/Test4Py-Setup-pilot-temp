import os
import mmap
import sys
import pytest
from thefuck.entrypoints.shell_logger import shell_logger, const

def test_shell_logger_no_shell(monkeypatch, caplog):
    """When SHELL is not set, shell_logger warns and exits with code 1."""
    monkeypatch.delenv("SHELL", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        shell_logger("/dev/null")
    assert excinfo.value.code == 1
    assert "Shell logger doesn't support your platform." in caplog.text

def test_shell_logger_creates_file_and_mmaps(tmp_path, monkeypatch):
    """shell_logger creates the log file with the correct size and maps it."""
    log_file = tmp_path / "logfile"
    # Set SHELL to a harmless shell that exits immediately
    monkeypatch.setenv("SHELL", "/bin/sh")
    # Ensure the shell exits with 0
    def fake_spawn(shell, read_func):
        # Simulate reading from the shell and then exit
        read_func()
        return 0
    monkeypatch.setattr("thefuck.entrypoints.shell_logger._spawn", fake_spawn)
    # Replace _read to just return immediately
    monkeypatch.setattr("thefuck.entrypoints.shell_logger._read", lambda buf: None)

    # Run shell_logger; it should exit with code 0
    with pytest.raises(SystemExit) as excinfo:
        shell_logger(str(log_file))
    assert excinfo.value.code == 0

    # Verify file exists and has the expected size
    assert log_file.exists()
    assert log_file.stat().st_size == const.LOG_SIZE_IN_BYTES

    # Verify that the file is memory‑mapped and writable
    with open(log_file, "rb") as f:
        mm = mmap.mmap(f.fileno(), const.LOG_SIZE_IN_BYTES, mmap.MAP_SHARED, mmap.PROT_WRITE)
        # The file should be zero‑filled initially
        assert mm.read(const.LOG_SIZE_IN_BYTES) == b'\x00' * const.LOG_SIZE_IN_BYTES
        mm.close()

def test_shell_logger_exits_with_shell_return_code(tmp_path, monkeypatch):
    """shell_logger exits with the return code of the spawned shell."""
    log_file = tmp_path / "logfile"
    monkeypatch.setenv("SHELL", "/bin/sh")
    # Simulate a shell that exits with code 42
    def fake_spawn(shell, read_func):
        read_func()
        return 42
    monkeypatch.setattr("thefuck.entrypoints.shell_logger._spawn", fake_spawn)
    monkeypatch.setattr("thefuck.entrypoints.shell_logger._read", lambda buf: None)

    with pytest.raises(SystemExit) as excinfo:
        shell_logger(str(log_file))
    assert excinfo.value.code == 42
