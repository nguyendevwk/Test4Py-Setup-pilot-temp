import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed should set default status, quiet flag and empty method."""
    exc = MethodNotAllowed()
    # status code from class attribute
    assert exc.status_code == 405
    # quiet defaults to True as defined in the class
    assert exc.quiet is True
    # method defaults to empty string
    assert exc.method == ""
    # allowed_methods should be None
    assert exc.allowed_methods is None
    # headers should contain at least the default ones from HTTPException
    assert isinstance(exc.headers, dict)
    # No Allow header when no allowed_methods provided
    assert "Allow" not in exc.headers


def test_allowed_methods_header_and_method():
    """Providing allowed_methods should set the Allow header and method attribute."""
    allowed = ["GET", "POST"]
    exc = MethodNotAllowed(method="PUT", allowed_methods=allowed)
    # method attribute set correctly
    assert exc.method == "PUT"
    # allowed_methods stored
    assert exc.allowed_methods == allowed
    # Allow header present and correctly formatted
    assert exc.headers.get("Allow") == "GET, POST"
    # No other unexpected headers
    assert set(exc.headers.keys()).issubset({"Allow"})


def test_custom_headers_merge():
    """Custom headers should be merged with the Allow header when allowed_methods is set."""
    custom = {"X-Custom": "value", "Allow": "OLD"}
    exc = MethodNotAllowed(allowed_methods=["DELETE"], headers=custom)
    # The Allow header should be overridden by the allowed_methods value
    assert exc.headers["Allow"] == "DELETE"
    # Custom header remains
    assert exc.headers["X-Custom"] == "value"
    # No duplicate Allow header
    assert list(exc.headers.keys()).count("Allow") == 1
