import pytest
from sanic.exceptions import NotFound


def test_notfound_default_initialization():
    """Verify that the default constructor sets the expected attributes."""
    exc = NotFound()
    # status_code should be 404 as defined in the class
    assert exc.status_code == 404
    # quiet defaults to True as defined in the class
    assert exc.quiet is True
    # message should be None when not provided
    assert exc.message is None
    # context and extra should be None by default
    assert exc.context is None
    assert exc.extra is None
    # headers should be None by default
    assert exc.headers is None


def test_notfound_with_message_and_headers():
    """Verify that providing a message and custom headers works correctly."""
    custom_headers = {"X-Custom": "value"}
    exc = NotFound("Page not found", headers=custom_headers)
    # message should be set to the provided string
    assert exc.message == "Page not found"
    # headers should be the dictionary we passed
    assert exc.headers == custom_headers
    # quiet should still be True by default
    assert exc.quiet is True
    # status_code remains 404
    assert exc.status_code == 404


def test_notfound_invalid_headers_type_raises():
    """Passing a non-dict type for headers should raise a TypeError."""
    with pytest.raises(TypeError):
        NotFound(headers=["not", "a", "dict"])
