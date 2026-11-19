import os
import mmap
import sys
import pytest
from pathlib import Path

# Import the target function and its dependencies
from thefuck.entrypoints.shell_logger import shell_logger, const, logs

@pytest.fixture
def tmp_log_file(tmp_path):
    """Provide a temporary file path for the logger."""
    return tmp_path / "logfile"

def test_shell_logger_exits_when_no_shell(monkeypatch, caplog):
    """When SHELL is not set, shell_logger should warn and exit."""
    # Ensure SHELL is unset
    monkeypatch.delenv("SHELL", raising=False)

    # Capture logs
    caplog.set_level("WARNING")

    with pytest.raises(SystemExit) as excinfo:
        shell_logger("dummy_output")

    # Verify exit code
    assert excinfo.value.code == 1

    # Verify warning message
    assert any(
        "Shell logger doesn't support your platform." in rec.message
        for rec in caplog.records
    )

def test_shell_logger_creates_file_and_mmaps(monkeypatch, tmp_log_file):
    """shell_logger should create a file of the correct size and mmap it."""
    # Set a dummy shell that exits immediately
    monkeypatch.setenv("SHELL", "/bin/sh")

    # Patch _spawn to simply return 0 without actually spawning a shell
    monkeypatch.setattr(
        "thefuck.entrypoints.shell_logger._spawn",
        lambda shell, read_func: 0
    )
    # Patch _read to do nothing
    monkeypatch.setattr(
        "thefuck.entrypoints.shell_logger._read",
        lambda buffer: None
    )

    # Run the logger; it will exit, so catch SystemExit
    with pytest.raises(SystemExit):
        shell_logger(str(tmp_log_file))

    # Verify the file was created
    assert tmp_log_file.exists()
    # Verify the file size matches LOG_SIZE_IN_BYTES
    assert tmp_log_file.stat().st_size == const.LOG_SIZE_IN_BYTES

    # Verify the file can be memory‑mapped and contains zero bytes
    with open(tmp_log_file, "rb") as f:
        data = f.read()
    assert data == b"\x00" * const.LOG_SIZE_IN_BYTES

def test_shell_logger_logs_warning_on_nonexistent_shell(monkeypatch, caplog, tmp_log_file):
    """If SHELL points to a non‑existent executable, shell_logger should warn and exit."""
    # Point SHELL to a non‑existent path
    monkeypatch.setenv("SHELL", "/nonexistent/shell")

    # Patch _spawn to raise FileNotFoundError to simulate missing shell
    def fake_spawn(shell, read_func):
        raise FileNotFoundError(f"{shell} not found")

    monkeypatch.setattr(
        "thefuck.entrypoints.shell_logger._spawn",
        fake_spawn
    )
    # Patch _read to do nothing
    monkeypatch.setattr(
        "thefuck.entrypoints.shell_logger._read",
        lambda buffer: None
    )

    caplog.set_level("ERROR")

    with pytest.raises(SystemExit) as excinfo:
        shell_logger(str(tmp_log_file))

    # Exit code should be 1 (default for unhandled exception)
    assert excinfo.value.code == 1

    # Verify error log contains the missing shell message
    assert any(
        "/nonexistent/shell not found" in rec.message
        for rec in caplog.records
    )
