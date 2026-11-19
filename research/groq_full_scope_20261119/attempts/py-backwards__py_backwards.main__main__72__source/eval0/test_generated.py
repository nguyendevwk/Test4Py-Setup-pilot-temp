import sys
import os
import importlib
import types
import pytest
from pathlib import Path

# Import the module under test
import py_backwards.main as main_module

@pytest.fixture
def reset_argv(monkeypatch):
    """Restore sys.argv after each test."""
    original = sys.argv.copy()
    yield
    sys.argv[:] = original

def test_main_success(tmp_path, reset_argv, capsys):
    # Create a simple input file
    src = tmp_path / "hello.py"
    src.write_text("print('hello')\n")
    # Output file path
    out = tmp_path / "out.py"
    # Prepare command line arguments
    sys.argv = [
        "py-backwards",
        "-i", str(src),
        "-o", str(out),
        "-t", "py36",
    ]
    # Run main
    exit_code = main_module.main()
    # Assertions
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Compilation finished" in captured.out
    assert out.exists()
    assert out.read_text() == "print('hello')\n"

def test_main_missing_input(tmp_path, reset_argv, capsys):
    # Non-existent input file
    src = tmp_path / "missing.py"
    out = tmp_path / "out.py"
    sys.argv = [
        "py-backwards",
        "-i", str(src),
        "-o", str(out),
        "-t", "py36",
    ]
    exit_code = main_module.main()
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "doesn't exist" in captured.err

def test_main_invalid_output(tmp_path, reset_argv, capsys):
    # Create a valid input file
    src = tmp_path / "hello.py"
    src.write_text("print('hello')\n")
    # Output path that is a directory
    out_dir = tmp_path / "out_dir"
    out_dir.mkdir()
    sys.argv = [
        "py-backwards",
        "-i", str(src),
        "-o", str(out_dir),
        "-t", "py36",
    ]
    exit_code = main_module.main()
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Invalid output" in captured.err
