import pytest
from sanic.exceptions import FileNotFound
from sanic.helpers import STATUS_CODES


def test_file_not_found_default_attributes(tmp_path):
    """FileNotFound should store default values correctly."""
    exc = FileNotFound()
    # Default message is None, so str(exc) should be the default status text
    assert str(exc) == STATUS_CODES[exc.status]
    # Path and relative_url default to None
    assert exc.path is None
    assert exc.relative_url is None
    # quiet, context, extra, headers default to None
    assert exc.quiet is None
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers is None
    # Status code should be 404
    assert exc.status == 404


def test_file_not_found_with_path_and_message(tmp_path):
    """Providing a message and path should set those attributes."""
    path = tmp_path / "missing.txt"
    message = "File not found: missing.txt"
    exc = FileNotFound(message=message, path=path)
    # The message should be stored in the base NotFound class
    assert exc.args[0] == message
    # Path should be stored as a PathLike object
    assert exc.path == path
    # relative_url remains None
    assert exc.relative_url is None
    # The string representation should include the message
    assert str(exc) == message


def test_file_not_found_with_headers_and_quiet(tmp_path):
    """Headers and quiet flag should be reflected in the exception."""
    headers = {"X-Custom-Header": "value"}
    exc = FileNotFound(quiet=True, headers=headers)
    # quiet flag should be stored
    assert exc.quiet is True
    # headers should be stored
    assert exc.headers == headers
    # The default message should still be the status text
    assert str(exc) == STATUS_CODES[exc.status]
