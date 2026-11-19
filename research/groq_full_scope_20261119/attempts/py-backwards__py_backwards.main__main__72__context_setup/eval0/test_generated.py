import builtins
import os
import sys
import types
import importlib
import pytest
from py_backwards import main as py_backwards_main
from py_backwards import const, exceptions, messages

# Helper to run main with custom argv and capture output
def run_main(argv, tmp_path, capsys):
    sys.argv = argv
    # Ensure tmp_path is used for any file operations
    return py_backwards_main.main(), capsys.readouterr()

def test_normal_compilation(tmp_path, capsys):
    # Create a simple input file that uses f-string (Python 3.6 feature)
    input_file = tmp_path / "hello.py"
    input_file.write_text('print(f"Hello {1+1}")\n')
    output_file = tmp_path / "out.py"

    # Run main
    exit_code, captured = run_main(
        ["prog", "-i", str(input_file), "-o", str(output_file), "-t", "py36"],
        tmp_path,
        capsys
    )

    # Assert successful exit
    assert exit_code == 0
    # Assert output file exists and contains transformed code
    assert output_file.exists()
    out_text = output_file.read_text()
    assert 'print("Hello 2")' in out_text
    # Assert compilation result message printed
    assert messages.compilation_result("1 file compiled") in captured.out

def test_missing_input_file(tmp_path, capsys):
    # Provide a non-existent input file
    missing_file = tmp_path / "does_not_exist.py"
    output_file = tmp_path / "out.py"

    exit_code, captured = run_main(
        ["prog", "-i", str(missing_file), "-o", str(output_file), "-t", "py36"],
        tmp_path,
        capsys
    )

    # Assert error exit
    assert exit_code == 1
    # Assert correct error message printed to stderr
    assert messages.input_doesnt_exists([str(missing_file)]) in captured.err

def test_invalid_output_path(tmp_path, capsys):
    # Create a valid input file
    input_file = tmp_path / "script.py"
    input_file.write_text('print("test")\n')
    # Use a directory as output path (invalid)
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    exit_code, captured = run_main(
        ["prog", "-i", str(input_file), "-o", str(output_dir), "-t", "py36"],
        tmp_path,
        capsys
    )

    # Assert error exit
    assert exit_code == 1
    # Assert invalid output error message printed
    assert messages.invalid_output([str(input_file)], str(output_dir)) in captured.err
