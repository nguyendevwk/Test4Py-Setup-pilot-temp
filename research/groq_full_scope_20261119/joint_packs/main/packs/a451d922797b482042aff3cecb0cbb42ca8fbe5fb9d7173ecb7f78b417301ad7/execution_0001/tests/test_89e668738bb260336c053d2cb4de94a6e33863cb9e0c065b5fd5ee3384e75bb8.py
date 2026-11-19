import pytest
from isort.exceptions import ExistingSyntaxErrors, ISortError
from pathlib import Path


def test_existing_syntax_errors_initialization(tmp_path: Path):
    """Verify that the exception stores the file path and constructs the message."""
    file_path = str(tmp_path / "example.py")
    exc = ExistingSyntaxErrors(file_path)
    assert exc.file_path == file_path
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)
    expected_msg = (
        f"isort was told to sort imports within code that contains syntax errors: {file_path}."
    )
    assert str(exc) == expected_msg


def test_existing_syntax_errors_message_contains_path(tmp_path: Path):
    """Ensure the error message always includes the provided file path."""
    file_path = str(tmp_path / "bad_syntax.py")
    exc = ExistingSyntaxErrors(file_path)
    assert file_path in str(exc)
    assert "syntax errors" in str(exc)


def test_existing_syntax_errors_with_non_string_path(tmp_path: Path):
    """Check that passing a non-string path still works and stores the string representation."""
    file_path_obj = tmp_path / "module.py"
    exc = ExistingSyntaxErrors(str(file_path_obj))
    assert exc.file_path == str(file_path_obj)
    assert str(exc).startswith("isort was told to sort imports within code that contains syntax errors:")
