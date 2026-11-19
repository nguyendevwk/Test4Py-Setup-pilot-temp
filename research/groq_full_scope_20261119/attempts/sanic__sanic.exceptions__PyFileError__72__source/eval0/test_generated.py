import pytest
from sanic.exceptions import PyFileError
from pathlib import Path

def test_pyfileerror_default_initialization(tmp_path: Path):
    """Verify default construction and message formatting."""
    test_file = tmp_path / "config.py"
    test_file.write_text("print('test')")

    exc = PyFileError(str(test_file))
    # Message should contain the file path
    assert str(test_file) in str(exc)
    # Default status_code should be None
    assert exc.status_code is None
    # quiet, context, extra, headers should be None by default
    assert exc.quiet is None
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers is None

def test_pyfileerror_with_all_parameters(tmp_path: Path):
    """Verify that all optional parameters are stored correctly."""
    test_file = tmp_path / "config.py"
    test_file.write_text("print('test')")

    context = {"user": "alice"}
    extra = {"debug": True}
    headers = {"X-Custom": "value"}

    exc = PyFileError(
        str(test_file),
        status_code=404,
        quiet=True,
        context=context,
        extra=extra,
        headers=headers,
    )
    assert exc.status_code == 404
    assert exc.quiet is True
    assert exc.context == context
    assert exc.extra == extra
    assert exc.headers == headers
    # Message should still contain the file path
    assert str(test_file) in str(exc)

def test_pyfileerror_message_representation(tmp_path: Path):
    """Ensure that the exception message uses the string representation of the file argument."""
    test_file = tmp_path / "config.py"
    test_file.write_text("print('test')")

    exc = PyFileError(test_file)
    # The message should use the string representation of the Path object
    assert "could not execute config file" in str(exc)
    assert str(test_file) in str(exc)
