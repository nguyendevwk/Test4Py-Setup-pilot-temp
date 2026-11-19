import pytest
from isort.exceptions import IntroducedSyntaxErrors, ISortError


def test_introduced_syntax_errors_initialization_and_message():
    """Verify that the exception stores the file path and formats the message correctly."""
    file_path = "example.py"
    exc = IntroducedSyntaxErrors(file_path)
    # The file_path attribute should be set
    assert exc.file_path == file_path
    # The message should contain the file path
    assert file_path in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith(
        "isort introduced syntax errors when attempting to sort the imports contained within "
    )


def test_introduced_syntax_errors_inherits_from_isort_error():
    """Ensure that IntroducedSyntaxErrors is a subclass of ISortError."""
    exc = IntroducedSyntaxErrors("dummy.py")
    assert isinstance(exc, ISortError)
    # ISortError is a subclass of Exception
    assert isinstance(exc, Exception)


def test_introduced_syntax_errors_repr_and_str_consistency():
    """Check that the string representation is consistent with the __repr__ output."""
    file_path = "test_module.py"
    exc = IntroducedSyntaxErrors(file_path)
    # The __repr__ should include the class name and the file path
    assert f"IntroducedSyntaxErrors(file_path='{file_path}')" in repr(exc)
    # The string representation should match the message in __repr__
    assert str(exc) in repr(exc)
