import pytest
from sanic.exceptions import FileNotFound
from sanic.helpers import STATUS_CODES

def test_file_not_found_basic_message_and_status():
    exc = FileNotFound("File missing")
    # The message should be stored in the exception
    assert str(exc) == "File missing"
    # The HTTP status code should be 404
    assert exc.status == 404
    # STATUS_CODES mapping should contain the description for 404
    assert STATUS_CODES[exc.status] == "Not Found"

def test_file_not_found_path_and_relative_url():
    exc = FileNotFound(path="/tmp/nonexistent.txt", relative_url="/files/nonexistent.txt")
    # Path and relative_url should be accessible as attributes
    assert exc.path == "/tmp/nonexistent.txt"
    assert exc.relative_url == "/files/nonexistent.txt"
    # The message defaults to None, so str(exc) should be empty
    assert str(exc) == ""

def test_file_not_found_with_headers_and_context():
    headers = {"X-Custom": "value"}
    context = {"user": "alice"}
    exc = FileNotFound("Missing", headers=headers, context=context)
    # Headers and context should be preserved
    assert exc.headers == headers
    assert exc.context == context
    # Quiet flag defaults to None
    assert exc.quiet is None
