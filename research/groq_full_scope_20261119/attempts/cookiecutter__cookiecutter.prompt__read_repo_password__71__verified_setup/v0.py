import io
import sys

import pytest

from cookiecutter.prompt import read_repo_password


def test_read_repo_password_returns_input(tmp_path):
    """When the user types a password, the function returns it unchanged."""
    # Simulate user typing "mysecret" followed by a newline
    sys.stdin = io.StringIO("mysecret\n")
    result = read_repo_password("Enter password:")
    assert result == "mysecret"
    # Restore original stdin
    sys.stdin = sys.__stdin__


def test_read_repo_password_empty_input(tmp_path):
    """If the user presses Enter without typing anything, an empty string is returned."""
    sys.stdin = io.StringIO("\n")
    result = read_repo_password("Enter password:")
    assert result == ""
    sys.stdin = sys.__stdin__


def test_read_repo_password_invalid_question_type():
    """Passing a non-string question raises a TypeError."""
    with pytest.raises(TypeError):
        read_repo_password(None)  # type: ignore[arg-type]
