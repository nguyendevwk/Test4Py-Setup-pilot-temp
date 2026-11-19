import pytest
from sanic.exceptions import URLBuildError


def test_urlbuilderror_basic_attributes():
    """URLBuildError should expose the expected default attributes."""
    exc = URLBuildError()
    # status_code is defined on the class
    assert exc.status_code == 500
    # message defaults to None
    assert exc.message is None
    # quiet, context, extra, headers default to None
    assert exc.quiet is None
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers is None
    # The string representation should include the status code
    assert "500" in str(exc)


def test_urlbuilderror_with_bytes_and_headers():
    """Passing a bytes message and custom headers should be preserved."""
    msg = b"binary error"
    headers = {"X-Custom": "value"}
    exc = URLBuildError(message=msg, headers=headers)
    # message should be stored as bytes
    assert isinstance(exc.message, bytes)
    assert exc.message == msg
    # headers should be stored as provided
    assert exc.headers == headers
    # quiet, context, extra remain None
    assert exc.quiet is None
    assert exc.context is None
    assert exc.extra is None
    # The exception string should include the bytes representation
    assert str(msg) in str(exc)


def test_urlbuilderror_raised_and_caught():
    """Raising URLBuildError should propagate the same instance."""
    try:
        raise URLBuildError(message="oops", quiet=True)
    except URLBuildError as e:
        # The caught exception should be the same instance
        assert e.message == "oops"
        assert e.quiet is True
        # status_code remains 500
        assert e.status_code == 500
        # context and extra default to None
        assert e.context is None
        assert e.extra is None
    else:
        pytest.fail("URLBuildError was not raised")
