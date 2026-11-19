import pytest
from isort.exceptions import IntroducedSyntaxErrors, ISortError


def test_introduced_syntax_errors_message_and_attribute(tmp_path):
    """Verify that the exception stores the file path and formats the message correctly."""
    test_file = tmp_path / "example.py"
    test_file.write_text("print('hello')")

    exc = IntroducedSyntaxErrors(str(test_file))
    # The file_path attribute should be set to the string path
    assert exc.file_path == str(test_file)
    # The message should contain the file path and the expected wording
    assert str(test_file) in str(exc)
    assert "isort introduced syntax errors" in str(exc)
    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)


def test_introduced_syntax_errors_empty_path():
    """An empty string should still produce a valid exception with an empty file_path."""
    exc = IntroducedSyntaxErrors("")
    assert exc.file_path == ""
    # The message should still contain the phrase but not raise an error
    assert "isort introduced syntax errors" in str(exc)
    # Ensure that the exception can be raised and caught normally
    with pytest.raises(IntroducedSyntaxErrors) as cm:
        raise exc
    assert cm.value is exc


def test_introduced_syntax_errors_non_string_input():
    """Passing a non-string should raise a TypeError during initialization."""
    with pytest.raises(TypeError):
        # The constructor expects a string; passing an int should fail
        IntroducedSyntaxErrors(123)
