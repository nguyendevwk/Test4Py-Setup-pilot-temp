import pytest
from sanic.exceptions import FileNotFound
from sanic.helpers import STATUS_CODES
from pathlib import Path


def test_file_not_found_basic_attributes():
    """Verify that FileNotFound stores the provided message, path and relative_url."""
    msg = "File missing"
    path = Path("/tmp/nonexistent.txt")
    rel_url = "/files/nonexistent.txt"

    exc = FileNotFound(message=msg, path=path, relative_url=rel_url)

    assert exc.args[0] == msg
    assert exc.path == path
    assert exc.relative_url == rel_url
    # The base NotFound exception should have status code 404
    assert exc.status == 404
    assert STATUS_CODES[exc.status] == "Not Found"


def test_file_not_found_bytes_message_and_headers():
    """Test that a bytes message and custom headers are preserved."""
    msg_bytes = b"Binary file not found"
    headers = {"X-Custom-Header": "value"}

    exc = FileNotFound(message=msg_bytes, headers=headers)

    assert exc.args[0] == msg_bytes
    assert exc.headers == headers
    # Ensure that the status code remains 404
    assert exc.status == 404


def test_file_not_found_invalid_path_type():
    """Passing a non-PathLike object should still be accepted but stored as is."""
    invalid_path = 12345  # int is not PathLike

    exc = FileNotFound(path=invalid_path)

    # The attribute should be set to the given value
    assert exc.path == invalid_path
    # No exception should be raised during initialization
    assert exc.status == 404
