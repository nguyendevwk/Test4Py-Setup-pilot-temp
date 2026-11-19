import sys
import io
import pytest
from cookiecutter.prompt import read_repo_password

def test_read_repo_password_normal(tmp_path):
    # Prepare a temporary file with a password and redirect stdin to it
    password = "s3cr3t"
    tmp_file = tmp_path / "input.txt"
    tmp_file.write_text(password + "\n")
    with open(tmp_file, "r") as f:
        with io.StringIO() as buf, io.StringIO() as err, \
             contextlib.redirect_stdin(f), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            result = read_repo_password("Enter password:")
    assert result == password

def test_read_repo_password_empty(tmp_path):
    # Test boundary case: user presses Enter without typing anything
    tmp_file = tmp_path / "empty.txt"
    tmp_file.write_text("\n")
    with open(tmp_file, "r") as f:
        with io.StringIO() as buf, io.StringIO() as err, \
             contextlib.redirect_stdin(f), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            result = read_repo_password("Enter password:")
    assert result == ""

def test_read_repo_password_invalid_question():
    # Passing a non-string question should raise a TypeError
    with pytest.raises(TypeError):
        read_repo_password(123)
