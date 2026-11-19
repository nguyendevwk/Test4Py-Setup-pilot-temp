import pytest
from isort.exceptions import ExistingSyntaxErrors


def test_message_includes_file_path(tmp_path):
    """The exception message should contain the provided file path."""
    file_path = tmp_path / "example.py"
    exc = ExistingSyntaxErrors(str(file_path))
    assert str(file_path) in str(exc), "Message does not contain the file path"
    assert f"{file_path}" in exc.args[0], "Exception args do not include the file path"


def test_file_path_attribute_and_type(tmp_path):
    """The exception should store the file path in a dedicated attribute."""
    file_path = tmp_path / "module.py"
    exc = ExistingSyntaxErrors(str(file_path))
    assert hasattr(exc, "file_path"), "Missing file_path attribute"
    assert exc.file_path == str(file_path), "file_path attribute does not match input"
    assert isinstance(exc.file_path, str), "file_path attribute is not a string"


def test_inheritance_and_non_string_input():
    """ExistingSyntaxErrors should inherit from Exception and handle non-string inputs gracefully."""
    # Passing a non-string (e.g., an integer) should still produce a string representation
    exc = ExistingSyntaxErrors(42)
    assert isinstance(exc, Exception), "ExistingSyntaxErrors is not an Exception subclass"
    assert "42" in str(exc), "String representation does not include the integer argument"
    # Passing None should also be handled without raising
    exc_none = ExistingSyntaxErrors(None)
    assert isinstance(exc_none, Exception), "ExistingSyntaxErrors is not an Exception subclass when given None"
    assert "None" in str(exc_none), "String representation does not include 'None' when given None"
