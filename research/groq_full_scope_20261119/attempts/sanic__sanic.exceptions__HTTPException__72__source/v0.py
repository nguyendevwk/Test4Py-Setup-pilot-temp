import pytest
from sanic.exceptions import HTTPException


def test_http_exception_initialization_with_all_kwargs():
    """Verify that HTTPException stores all provided keyword arguments correctly."""
    message = "Test error"
    quiet = True
    context = {"user_id": 42}
    extra = {"debug": True}
    headers = {"X-Custom-Header": "value"}

    exc = HTTPException(
        message,
        quiet=quiet,
        context=context,
        extra=extra,
        headers=headers,
    )

    # The exception should be an instance of Exception and HTTPException
    assert isinstance(exc, Exception)
    assert isinstance(exc, HTTPException)

    # The message should be stored as the exception's args[0]
    assert exc.args[0] == message

    # Custom attributes should be accessible
    assert getattr(exc, "quiet", None) is quiet
    assert getattr(exc, "context", None) == context
    assert getattr(exc, "extra", None) == extra
    assert getattr(exc, "headers", None) == headers


def test_http_exception_message_bytes_and_none():
    """Ensure that message can be bytes or None and is handled correctly."""
    # Bytes message
    bytes_msg = b"Binary error"
    exc_bytes = HTTPException(bytes_msg)
    assert exc_bytes.args[0] == bytes_msg

    # None message defaults to None
    exc_none = HTTPException()
    assert exc_none.args[0] is None


def test_http_exception_raised_and_caught():
    """Raise HTTPException and catch it, verifying the exception type and message."""
    with pytest.raises(HTTPException) as excinfo:
        raise HTTPException("Raised error")

    caught_exc = excinfo.value
    assert isinstance(caught_exc, HTTPException)
    assert caught_exc.args[0] == "Raised error"
