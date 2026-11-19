import pytest
from isort.exceptions import ExistingSyntaxErrors
from isort.exceptions import ISortError

def test_existing_syntax_errors_initialization(tmp_path):
    # Create a temporary file path to use in the exception
    file_path = tmp_path / "bad.py"
    file_path.write_text("def foo(:\n    pass")  # intentionally bad syntax
    exc = ExistingSyntaxErrors(str(file_path))
    # The exception should store the file path correctly
    assert exc.file_path == str(file_path)
    # The message should contain the file path
    assert str(file_path) in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith("isort was told to sort imports within code that contains syntax errors:")

def test_existing_syntax_errors_inheritance():
    # ExistingSyntaxErrors should be a subclass of ISortError
    assert issubclass(ExistingSyntaxErrors, ISortError)
    # An instance should be recognized as an ISortError
    exc = ExistingSyntaxErrors("dummy.py")
    assert isinstance(exc, ISortError)

def test_existing_syntax_errors_repr_and_str():
    # The string representation should be the same as the message
    exc = ExistingSyntaxErrors("example.py")
    message = "isort was told to sort imports within code that contains syntax errors: example.py."
    assert str(exc) == message
    # The repr should include the class name and the message
    assert repr(exc).startswith("<isort.exceptions.ExistingSyntaxErrors")
    assert message in repr(exc)
