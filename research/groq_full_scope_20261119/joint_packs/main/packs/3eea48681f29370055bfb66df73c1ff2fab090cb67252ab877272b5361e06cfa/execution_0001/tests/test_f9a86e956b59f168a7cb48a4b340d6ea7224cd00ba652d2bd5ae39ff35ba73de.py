import pytest
from pathlib import Path
from isort.exceptions import ExistingSyntaxErrors, ISortError


def test_existing_syntax_errors_message_and_attribute(tmp_path: Path):
    """Verify that the error message contains the file path and the attribute is set."""
    file_path = tmp_path / "bad.py"
    exc = ExistingSyntaxErrors(str(file_path))
    assert exc.file_path == str(file_path)
    assert str(file_path) in str(exc)
    assert "syntax errors" in str(exc)


def test_existing_syntax_errors_inheritance():
    """Ensure ExistingSyntaxErrors is a subclass of ISortError."""
    exc = ExistingSyntaxErrors("dummy.py")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_existing_syntax_errors_with_non_string_file_path():
    """Passing a non-string file path should still store the value and produce a message."""
    non_string_path = 12345
    exc = ExistingSyntaxErrors(non_string_path)  # type: ignore[arg-type]
    # The file_path attribute should be the non-string value
    assert exc.file_path == non_string_path
    # The message should include the string representation of the non-string value
    assert str(non_string_path) in str(exc)
