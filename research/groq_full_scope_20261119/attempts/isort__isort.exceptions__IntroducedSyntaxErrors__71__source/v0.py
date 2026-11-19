import pytest
from isort.exceptions import IntroducedSyntaxErrors
from isort.exceptions import ISortError

def test_introduced_syntax_errors_initialization(tmp_path):
    # Create a temporary file path to use in the exception
    file_path = tmp_path / "example.py"
    file_path.write_text("print('hello')")

    exc = IntroducedSyntaxErrors(str(file_path))

    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)

    # The file_path attribute should be set correctly
    assert exc.file_path == str(file_path)

    # The message should contain the file path
    assert str(file_path) in str(exc)

def test_introduced_syntax_errors_message_content():
    # Use a simple string as the file path
    file_path = "/path/to/file.py"
    exc = IntroducedSyntaxErrors(file_path)

    # The message should start with the expected prefix
    expected_prefix = "isort introduced syntax errors when attempting to sort the imports contained within"
    assert str(exc).startswith(expected_prefix)

    # The message should end with the file path
    assert str(exc).endswith(file_path)

    # The message should not contain any unintended substrings
    assert "unexpected" not in str(exc)

def test_introduced_syntax_errors_repr_and_str():
    file_path = "module.py"
    exc = IntroducedSyntaxErrors(file_path)

    # The __repr__ should include the class name and file path
    repr_str = repr(exc)
    assert "IntroducedSyntaxErrors" in repr_str
    assert file_path in repr_str

    # The __str__ should be identical to the message
    assert str(exc) == exc.args[0]
