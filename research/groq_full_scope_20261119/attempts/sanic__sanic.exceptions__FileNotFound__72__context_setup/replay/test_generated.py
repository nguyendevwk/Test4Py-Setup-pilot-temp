import pytest
from sanic.exceptions import FileNotFound


def test_file_not_found_default_message_and_status():
    """FileNotFound should default to the HTTP 404 status and use the default message."""
    exc = FileNotFound()
    # The base NotFound sets status_code to 404
    assert exc.status_code == 404
    # When message is None, the exception message should be the default status text
    # SanicException uses STATUS_CODES mapping; we check that the message is not empty
    assert isinstance(exc.message, str) and exc.message != ""
    # The quiet flag should default to True as defined in NotFound
    assert exc.quiet is True


def test_file_not_found_path_and_relative_url_assignment(tmp_path):
    """FileNotFound should store the provided path and relative_url attributes."""
    # Create a temporary file to use as a path
    temp_file = tmp_path / "test.txt"
    temp_file.write_text("content")
    # Use a relative URL
    rel_url = "/static/test.txt"
    exc = FileNotFound(message="File missing", path=temp_file, relative_url=rel_url)
    # Path should be stored as a PathLike object
    assert exc.path == temp_file
    # Relative URL should be stored exactly
    assert exc.relative_url == rel_url
    # The message should be preserved
    assert exc.message == "File missing"


def test_file_not_found_headers_and_context():
    """FileNotFound should accept custom headers and context and expose them."""
    headers = {"X-Custom-Header": "value"}
    context = {"user": "alice"}
    exc = FileNotFound(message="Not found", headers=headers, context=context)
    # Headers should be stored in the exception
    assert exc.headers == headers
    # Context should be stored in the exception
    assert exc.context == context
    # The message should be preserved
    assert exc.message == "Not found"
