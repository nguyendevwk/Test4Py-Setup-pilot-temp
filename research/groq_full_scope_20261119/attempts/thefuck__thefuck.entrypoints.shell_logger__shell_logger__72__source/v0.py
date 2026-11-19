import os
import sys
import mmap
import pytest
from thefuck.entrypoints.shell_logger import shell_logger, const, logs

def test_shell_logger_no_shell(monkeypatch, caplog):
    # Ensure SHELL is not set
    monkeypatch.delenv('SHELL', raising=False)
    # Capture logs
    caplog.set_level(logs.warn.__name__)
    # Expect SystemExit with code 1
    with pytest.raises(SystemExit) as excinfo:
        shell_logger('/dev/null')
    assert excinfo.value.code == 1
    # Verify warning message logged
    assert any("Shell logger doesn't support your platform." in rec.message for rec in caplog.records)

def test_shell_logger_creates_file(tmp_path, monkeypatch):
    # Set SHELL to a harmless shell
    monkeypatch.setenv('SHELL', '/bin/sh')
    # Use a temporary file
    output_file = tmp_path / "logfile"
    # Run shell_logger in a subprocess to avoid exiting the test process
    import subprocess, shlex
    cmd = f"{sys.executable} -c \"import thefuck.entrypoints.shell_logger as sl; sl.shell_logger('{output_file}')\""
    result = subprocess.run(shlex.split(cmd), capture_output=True)
    # shell_logger should exit with 0
    assert result.returncode == 0
    # File should exist and have the expected size
    assert output_file.exists()
    assert output_file.stat().st_size == const.LOG_SIZE_IN_BYTES
    # File should be zeroed
    with open(output_file, 'rb') as f:
        data = f.read()
    assert data == b'\x00' * const.LOG_SIZE_IN_BYTES

def test_shell_logger_file_permissions(tmp_path, monkeypatch):
    # Set SHELL to a harmless shell
    monkeypatch.setenv('SHELL', '/bin/sh')
    output_file = tmp_path / "logfile"
    # Run shell_logger
    import subprocess, shlex
    cmd = f"{sys.executable} -c \"import thefuck.entrypoints.shell_logger as sl; sl.shell_logger('{output_file}')\""
    subprocess.run(shlex.split(cmd), check=True)
    # Verify that the file is readable and writable by the owner
    mode = os.stat(output_file).st_mode
    assert mode & 0o600 == 0o600
