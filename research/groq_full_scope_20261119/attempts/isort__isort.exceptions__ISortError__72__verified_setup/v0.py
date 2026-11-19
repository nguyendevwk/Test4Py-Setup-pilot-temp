import pytest
from isort.exceptions import ISortError
from pathlib import Path


def test_isort_error_message_and_inheritance():
    """ISortError should store the message and be a subclass of Exception."""
    msg = "Something went wrong"
    err = ISortError(msg)
    assert isinstance(err, Exception)
    assert str(err) == msg
    assert err.args == (msg,)


def test_isort_error_reduce_and_reconstruction(tmp_path: Path):
    """The __reduce__ method should allow pickling and reconstruction of the error."""
    # Create a temporary file to use as part of the error state
    temp_file = tmp_path / "dummy.py"
    temp_file.write_text("print('hello')")

    # Instantiate the error with a message and a file path
    err = ISortError(f"Failed to process {temp_file}")
    # Attach the file path to the error instance for testing __reduce__
    err.file_path = temp_file

    # Use the reduce method to get the callable and arguments
    reduce_callable, reduce_args = err.__reduce__()
    # Reconstruct the error using the callable and arguments
    reconstructed_err = reduce_callable(*reduce_args)

    # The reconstructed error should have the same message and attributes
    assert isinstance(reconstructed_err, ISortError)
    assert str(reconstructed_err) == str(err)
    assert getattr(reconstructed_err, "file_path", None) == temp_file


def test_isort_error_with_empty_message_and_context():
    """ISortError should handle empty messages and additional context gracefully."""
    err = ISortError("")
    # Empty message should still be a valid string representation
    assert str(err) == ""
    # Adding arbitrary context should not affect the base error behavior
    err.context = "additional info"
    assert getattr(err, "context") == "additional info"
    # The error should still be caught as an Exception
    with pytest.raises(ISortError):
        raise err
