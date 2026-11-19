import pytest
from pathlib import Path
from isort.exceptions import UnsupportedEncoding

def test_unsupported_encoding_with_string(tmp_path):
    """Creating the exception with a string filename stores the name and formats the message."""
    filename = "test_file.py"
    exc = UnsupportedEncoding(filename)
    assert isinstance(exc, UnsupportedEncoding)
    assert exc.filename == filename
    assert str(exc) == f"Unknown or unsupported encoding in {filename}"
    # The message should contain the filename
    assert filename in str(exc)

def test_unsupported_encoding_with_path(tmp_path):
    """Creating the exception with a Path object stores the Path and formats the message."""
    file_path = tmp_path / "example.py"
    file_path.write_text("print('hello')")
    exc = UnsupportedEncoding(file_path)
    assert isinstance(exc, UnsupportedEncoding)
    # The filename attribute should be the Path object
    assert exc.filename == file_path
    # The message should use the Path's string representation
    assert str(exc) == f"Unknown or unsupported encoding in {file_path}"
    # The message should contain the string representation of the Path
    assert str(file_path) in str(exc)

def test_unsupported_encoding_with_invalid_type():
    """Passing an unsupported type (e.g., int) still constructs the exception but may raise TypeError when used."""
    invalid_input = 12345
    exc = UnsupportedEncoding(invalid_input)
    # The filename attribute stores the original value
    assert exc.filename == invalid_input
    # The message should convert the value to string
    assert str(exc) == f"Unknown or unsupported encoding in {invalid_input}"
    # Ensure that the exception is still an instance of UnsupportedEncoding
    assert isinstance(exc, UnsupportedEncoding)
