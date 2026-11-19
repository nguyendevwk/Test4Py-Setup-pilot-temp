import os
import sys
import stat
import pytest
from py_backwards import main as py_backwards_main
from py_backwards import compiler, const, exceptions, messages

@pytest.fixture
def simple_py(tmp_path):
    """Create a minimal Python file that can be compiled."""
    file_path = tmp_path / "hello.py"
    file_path.write_text("print('hello world')\n")
    return file_path

def test_main_success(tmp_path, simple_py, monkeypatch, capsys):
    """Normal execution: compile a single file and verify success."""
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    # Prepare command line arguments
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(simple_py),
        "-o", str(output_dir),
        "-t", "py36",
    ])
    # Run main
    exit_code = py_backwards_main.main()
    # Capture output
    out, err = capsys.readouterr()
    # Assertions
    assert exit_code == 0
    assert err == ""
    # The output directory should contain a compiled file
    compiled_files = list(output_dir.glob("*.py"))
    assert len(compiled_files) == 1
    # The compilation result message should mention the file
    assert simple_py.name in out
    assert "compiled" in out.lower()

def test_main_input_doesnt_exist(tmp_path, monkeypatch, capsys):
    """Error when input file does not exist."""
    non_existent = tmp_path / "does_not_exist.py"
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(non_existent),
        "-o", str(output_dir),
        "-t", "py36",
    ])
    exit_code = py_backwards_main.main()
    out, err = capsys.readouterr()
    assert exit_code == 1
    assert err == messages.input_doesnt_exists([str(non_existent)]) + "\n"
    assert out == ""

def test_main_permission_error(tmp_path, simple_py, monkeypatch, capsys):
    """Error when output path is not writable (PermissionError)."""
    # Create a file and make it read-only
    output_file = tmp_path / "readonly.py"
    output_file.write_text("")
    os.chmod(output_file, stat.S_IREAD)
    monkeypatch.setattr(sys, "argv", [
        "py-backwards",
        "-i", str(simple_py),
        "-o", str(output_file),
        "-t", "py36",
    ])
    exit_code = py_backwards_main.main()
    out, err = capsys.readouterr()
    assert exit_code == 1
    assert err == messages.permission_error(str(output_file)) + "\n"
    assert out == ""
