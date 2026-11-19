import os
import sys
import mmap
import signal
import pytest
from thefuck.entrypoints.shell_logger import shell_logger, const, logs


def test_shell_logger_creates_file_and_exits_zero(tmp_path, monkeypatch, capsys):
    """When SHELL is set, shell_logger should create the log file and exit with the shell's return code."""
    # Arrange
    output_file = tmp_path / "logfile"
    monkeypatch.setenv("SHELL", "/bin/sh")
    # Capture SystemExit
    with pytest.raises(SystemExit) as excinfo:
        shell_logger(str(output_file))
    # Assert exit code
    assert excinfo.value.code == 0
    # Assert file exists and has correct size
    assert output_file.exists()
    assert output_file.stat().st_size == const.LOG_SIZE_IN_BYTES
    # Verify that the file contains at least some data written by the shell
    with mmap.mmap(output_file.open("rb").fileno(), 0, access=mmap.ACCESS_READ) as mm:
        assert mm.read(1) != b'\x00'  # shell writes something non‑zero


def test_shell_logger_respects_log_size(tmp_path, monkeypatch):
    """The log file should be exactly LOG_SIZE_IN_BYTES bytes long."""
    output_file = tmp_path / "logfile"
    monkeypatch.setenv("SHELL", "/bin/sh")
    with pytest.raises(SystemExit):
        shell_logger(str(output_file))
    assert output_file.stat().st_size == const.LOG_SIZE_IN_BYTES


def test_shell_logger_no_shell_env(monkeypatch, caplog):
    """If SHELL is not defined, shell_logger should warn and exit with code 1."""
    monkeypatch.delenv("SHELL", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        shell_logger("dummy")
    assert excinfo.value.code == 1
    assert any("Shell logger doesn't support your platform." in rec.message for rec in caplog.records)
