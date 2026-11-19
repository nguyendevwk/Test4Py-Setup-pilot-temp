import sys
import os
import importlib
import types
import pytest
from pathlib import Path

# Import the module under test
import py_backwards.main as main_module

@pytest.fixture
def reset_sys_argv():
    original = sys.argv
    yield
    sys.argv = original

def test_main_success(tmp_path, capsys, reset_sys_argv):
    # Create a simple Python file that uses an f-string (Python 3.6 feature)
    src_file = tmp_path / "hello.py"
    src_file.write_text('print(f"Hello, {1+1}")\n')

    # Output directory
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Prepare command line arguments
    sys.argv = [
        "py-backwards",
        "-i", str(src_file),
        "-o", str(out_dir),
        "-t", "3.5",  # target version
    ]

    # Run main
    exit_code = main_module.main()

    # Verify exit code is 0
    assert exit_code == 0

    # Verify output file exists
    out_file = out_dir / src_file.name
    assert out_file.exists()

    # Verify that the output file contains the transformed code
    # (the exact transformation is not specified, but it should not contain the original f-string)
    out_text = out_file.read_text()
    assert 'f"Hello' not in out_text
    assert 'Hello, 2' in out_text

    # Verify that a compilation result message was printed
    captured = capsys.readouterr()
    assert "Compilation finished" in captured.out

def test_main_input_doesnt_exist(tmp_path, capsys, reset_sys_argv):
    # Non-existent input file
    fake_file = tmp_path / "does_not_exist.py"

    # Output directory
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    sys.argv = [
        "py-backwards",
        "-i", str(fake_file),
        "-o", str(out_dir),
        "-t", "3.5",
    ]

    exit_code = main_module.main()

    # Exit code should be 1 for error
    assert exit_code == 1

    # Error message should mention the missing input
    captured = capsys.readouterr()
    assert "does_not_exist.py" in captured.err
    assert "doesn't exist" in captured.err

def test_main_invalid_input_output(tmp_path, capsys, reset_sys_argv):
    # Create a source file
    src_file = tmp_path / "script.py"
    src_file.write_text('print("test")\n')

    # Output path is a file, but input is a file (valid) – this should be fine
    # To trigger InvalidInputOutput, we need input as a directory and output as a file
    src_dir = tmp_path / "src_dir"
    src_dir.mkdir()
    (src_dir / "mod.py").write_text('print("mod")\n')

    out_file = tmp_path / "output.py"  # file instead of directory

    sys.argv = [
        "py-backwards",
        "-i", str(src_dir),
        "-o", str(out_file),
        "-t", "3.5",
    ]

    exit_code = main_module.main()

    # Exit code should be 1 for error
    assert exit_code == 1

    # Error message should mention invalid output
    captured = capsys.readouterr()
    assert "invalid output" in captured.err
    assert str(out_file) in captured.err
