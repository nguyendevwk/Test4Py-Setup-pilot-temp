import io
import os
import sys
import tempfile
import pytest
from tornado import options

def test_print_help_to_stderr(capsys):
    """print_help writes to stderr by default."""
    options.print_help()
    captured = capsys.readouterr()
    # stderr should contain the help header
    assert "Options:" in captured.err
    # ensure no output to stdout
    assert captured.out == ""

def test_print_help_to_file(tmp_path):
    """print_help writes to a provided file-like object."""
    file_path = tmp_path / "help.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        options.print_help(f)
    content = file_path.read_text(encoding="utf-8")
    # The file should contain the help header
    assert "Options:" in content
    # Ensure the file is not empty
    assert len(content) > 0

def test_print_help_invalid_file_raises():
    """print_help raises an exception when the file is not writable."""
    # Create a read-only temporary file
    fd, path = tempfile.mkstemp()
    os.close(fd)
    os.chmod(path, 0o444)  # read-only
    with pytest.raises(OSError):
        with open(path, "w") as f:
            options.print_help(f)
    os.remove(path)
