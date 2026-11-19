import pytest
from isort.exceptions import ExistingSyntaxErrors, ISortError


def test_existing_syntax_errors_initialization(tmp_path):
    """Verify that the exception stores the file path and constructs the message correctly."""
    file_path = str(tmp_path / "bad.py")
    exc = ExistingSyntaxErrors(file_path)
    # The file_path attribute should be set
    assert exc.file_path == file_path
    # The message should contain the file path
    assert file_path in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith("isort was told to sort imports within code that contains syntax errors:")


def test_existing_syntax_errors_inherits_from_isort_error():
    """Ensure that ExistingSyntaxErrors is a subclass of ISortError and Exception."""
    exc = ExistingSyntaxErrors("dummy.py")
    # Check subclass relationships
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)
    # The base class should not be instantiated directly
    with pytest.raises(TypeError):
        ISortError()


def test_existing_syntax_errors_repr_and_str_consistency():
    """The string representation should be consistent with the message attribute."""
    file_path = "example.py"
    exc = ExistingSyntaxErrors(file_path)
    # The __str__ should match the message passed to the base Exception
    assert str(exc) == exc.args[0]
    # The repr should include the class name and the message
    assert repr(exc).startswith(f"<{ExistingSyntaxErrors.__name__}")
    assert file_path in repr(exc)
