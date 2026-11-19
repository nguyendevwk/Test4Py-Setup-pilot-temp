import pytest
from isort.exceptions import IntroducedSyntaxErrors, ISortError


def test_introduced_syntax_errors_message_and_attribute():
    """Verify that the exception message contains the file path and the attribute is set."""
    file_path = "example.py"
    exc = IntroducedSyntaxErrors(file_path)
    # The message should mention the file path
    assert file_path in str(exc)
    # The file_path attribute should be stored correctly
    assert exc.file_path == file_path


def test_introduced_syntax_errors_inherits_from_isort_error_and_exception():
    """Ensure the exception inherits from ISortError and the built‑in Exception."""
    exc = IntroducedSyntaxErrors("dummy.py")
    # ISortError is the direct parent
    assert isinstance(exc, ISortError)
    # Exception is an ancestor
    assert isinstance(exc, Exception)


def test_introduced_syntax_errors_raises_with_invalid_type():
    """Confirm that passing a non‑string file path still creates the exception but the message reflects the type."""
    non_string = 123
    exc = IntroducedSyntaxErrors(non_string)
    # The string representation should include the non‑string value
    assert str(non_string) in str(exc)
    # The file_path attribute should store the original value
    assert exc.file_path == non_string
