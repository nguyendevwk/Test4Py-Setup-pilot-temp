import os
import mmap
import sys
import pytest
from pathlib import Path
from thefuck.entrypoints.shell_logger import shell_logger, const, logs

@pytest.fixture
def tmp_log_file(tmp_path):
    return tmp_path / "logfile"

def test_shell_logger_no_shell_env(monkeypatch, caplog):
    """When SHELL is not set, shell_logger warns and exits."""
    monkeypatch.delenv("SHELL", raising=False)
    caplog.set_level(logs.warn.__name__)
    with pytest.raises(SystemExit) as excinfo:
        shell_logger("dummy_output")
    assert excinfo.value.code == 1
    assert any("Shell logger doesn't support your platform." in rec.message for rec in caplog.records)

def test_shell_logger_creates_and_truncates_file(tmp_log_file, monkeypatch):
    """shell_logger creates the output file and truncates it to LOG_SIZE_IN_BYTES."""
    # Ensure SHELL is set to a harmless command
    monkeypatch.setenv("SHELL", "/bin/true")
    # Run shell_logger; it will exit after spawning the shell
    with pytest.raises(SystemExit):
        shell_logger(str(tmp_log_file))
    # Verify file exists and has the expected size
    assert tmp_log_file.exists()
    assert tmp_log_file.stat().st_size == const.LOG_SIZE_IN_BYTES
    # Verify the file is zeroed out
    with mmap.mmap(tmp_log_file.open("rb").fileno(), 0, access=mmap.ACCESS_READ) as mm:
        assert mm.read() == b'\x00' * const.LOG_SIZE_IN_BYTES

def test_shell_logger_returns_shell_exit_code(tmp_log_file, monkeypatch):
    """shell_logger returns the exit code of the spawned shell."""
    # Use a shell that exits with a known code
    monkeypatch.setenv("SHELL", "/bin/sh")
    # Create a temporary script that exits with code 42
    script = tmp_log_file.parent / "exit42.sh"
    script.write_text("#!/bin/sh\nexit 42\n")
    script.chmod(0o755)
    # Monkeypatch the SHELL to run the script
    monkeypatch.setenv("SHELL", str(script))
    with pytest.raises(SystemExit) as excinfo:
        shell_logger(str(tmp_log_file))
    assert excinfo.value.code == 42
