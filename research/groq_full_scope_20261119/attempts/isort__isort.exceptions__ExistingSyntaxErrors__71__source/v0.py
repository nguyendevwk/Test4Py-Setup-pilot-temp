import pytest
from isort.exceptions import ExistingSyntaxErrors
from isort.exceptions import ISortError

def test_existing_syntax_errors_initialization(tmp_path):
    # Create a temporary file path to use in the exception
    file_path = tmp_path / "bad.py"
    file_path.write_text("def bad code")

    # Instantiate the exception with the file path
    exc = ExistingSyntaxErrors(str(file_path))

    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)

    # The file_path attribute should be set correctly
    assert exc.file_path == str(file_path)

    # The message should contain the file path
    assert str(file_path) in str(exc)

def test_existing_syntax_errors_message_content():
    # Use a simple file path string
    file_path = "/path/to/file.py"

    # Instantiate the exception
    exc = ExistingSyntaxErrors(file_path)

    # The message should start with the expected prefix
    expected_start = f"isort was told to sort imports within code that contains syntax errors: {file_path}."
    assert str(exc) == expected_start

    # The message should not contain any unexpected substrings
    assert "unexpected" not in str(exc)

def test_existing_syntax_errors_attribute_access():
    # Instantiate with a known file path
    file_path = "example.py"
    exc = ExistingSyntaxErrors(file_path)

    # Access the file_path attribute directly
    assert exc.file_path == file_path

    # Ensure that accessing a non-existent attribute raises AttributeError
    with pytest.raises(AttributeError):
        _ = exc.non_existent_attribute
