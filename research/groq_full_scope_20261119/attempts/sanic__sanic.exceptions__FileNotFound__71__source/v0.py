import pytest
from sanic.exceptions import FileNotFound
from sanic.helpers import STATUS_CODES

# Test 1: Basic construction and attribute assignment
def test_file_not_found_basic_attributes():
    exc = FileNotFound("File missing", path="/tmp/missing.txt", relative_url="/missing.txt")
    assert isinstance(exc, FileNotFound)
    assert exc.message == "File missing"
    assert exc.path == "/tmp/missing.txt"
    assert exc.relative_url == "/missing.txt"
    # Default status code should be 404
    assert exc.status == 404
    assert STATUS_CODES[exc.status] == "Not Found"

# Test 2: Headers propagation and quiet flag
def test_file_not_found_headers_and_quiet():
    headers = {"X-Custom": "value"}
    exc = FileNotFound(quiet=True, headers=headers)
    # quiet flag should be stored on the exception
    assert getattr(exc, "quiet", None) is True
    # headers should be accessible via the headers attribute
    assert exc.headers == headers
    # message defaults to None, but status remains 404
    assert exc.message is None
    assert exc.status == 404

# Test 3: Context and extra data handling
def test_file_not_found_context_and_extra():
    context = {"user": "alice"}
    extra = {"debug": True}
    exc = FileNotFound(context=context, extra=extra)
    # context and extra should be stored on the exception
    assert exc.context == context
    assert exc.extra == extra
    # Ensure that the exception can be converted to a dict (common in Sanic)
    # The dict representation should include the status and message
    exc_dict = exc.to_dict()
    assert exc_dict["status"] == 404
    assert exc_dict["message"] == exc.message
    # context and extra should be present in the dict
    assert exc_dict["context"] == context
    assert exc_dict["extra"] == extra
