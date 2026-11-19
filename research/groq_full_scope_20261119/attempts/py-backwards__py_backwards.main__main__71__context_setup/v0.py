import sys
import os
import io
import pytest
from py_backwards.main import main
from py_backwards import exceptions, messages

@pytest.fixture
def simple_py(tmp_path):
    """Create a minimal Python file using a f-string."""
    file_path = tmp_path / "sample.py"
    file_path.write_text('print(f"Hello {1+1}")\n')
    return file_path

def test_main_success(tmp_path, simple_py, monkeypatch, capsys):
    """Test that main compiles a simple file and returns 0."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    # Simulate command line arguments
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(simple_py),
        "-o", str(output_dir),
        "-t", "py36",  # assume py36 is a valid target
    ])
    ret = main()
    captured = capsys.readouterr()
    # The result message should be printed to stdout
    assert ret == 0
    assert "Compilation finished" in captured.out
    # The output file should exist
    out_file = output_dir / simple_py.name
    assert out_file.exists()
    # The compiled content should not contain the original f-string
    compiled = out_file.read_text()
    assert 'f"Hello' not in compiled

def test_main_input_doesnt_exist(tmp_path, monkeypatch, capsys):
    """Test that providing a non‑existent input file triggers the correct error."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    fake_input = tmp_path / "does_not_exist.py"
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(fake_input),
        "-o", str(output_dir),
        "-t", "py36",
    ])
    ret = main()
    captured = capsys.readouterr()
    assert ret == 1
    assert messages.syntax_error(exceptions.CompilationError("")).strip() in captured.err
    # No output file should be created
    assert not any(output_dir.iterdir())

def test_main_invalid_input_output(tmp_path, simple_py, monkeypatch, capsys):
    """Test that using the same file for input and output triggers InvalidInputOutput."""
    # Use the same path for input and output
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(simple_py),
        "-o", str(simple_py),
        "-t", "py36",
    ])
    ret = main()
    captured = capsys.readouterr()
    assert ret == 1
    assert messages.invalid_output([str(simple_py)], str(simple_py)) in captured.err
