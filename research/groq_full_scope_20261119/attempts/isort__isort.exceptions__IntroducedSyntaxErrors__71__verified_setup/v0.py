import pytest
from isort.exceptions import IntroducedSyntaxErrors, ISortError


def test_introduced_syntax_errors_message_and_attribute(tmp_path):
    """Verify that the exception message contains the file path and the attribute is set."""
    file_path = str(tmp_path / "example.py")
    exc = IntroducedSyntaxErrors(file_path)
    # The message should mention the file path
    assert file_path in str(exc)
    # The file_path attribute should be stored correctly
    assert exc.file_path == file_path


def test_introduced_syntax_errors_inheritance():
    """Ensure IntroducedSyntaxErrors inherits from ISortError."""
    assert issubclass(IntroducedSyntaxErrors, ISortError)


def test_introduced_syntax_errors_with_empty_path():
    """Check behavior when an empty string is passed as the file path."""
    with pytest.raises(ValueError):
        # The constructor should raise ValueError for an empty path
        IntroducedSyntaxErrors("")
