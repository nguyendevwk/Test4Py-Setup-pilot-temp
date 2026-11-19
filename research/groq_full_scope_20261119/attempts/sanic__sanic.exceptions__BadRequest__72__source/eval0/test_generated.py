import pytest
from sanic.exceptions import BadRequest


def test_badrequest_basic():
    """Verify that a BadRequest instance has the correct default attributes."""
    exc = BadRequest()
    # status_code and quiet are class attributes
    assert exc.status_code == 400
    assert exc.quiet is True
    # message defaults to None
    assert exc.message is None
    # headers default to empty dict
    assert exc.headers == {}
    # context and extra default to None
    assert exc.context is None
    assert exc.extra is None


def test_badrequest_with_context_and_headers():
    """Verify that context, extra, and headers are stored correctly."""
    headers = {"X-Test": "value"}
    context = {"user_id": 123}
    extra = {"debug": True}
    exc = BadRequest(
        message="Invalid input",
        context=context,
        extra=extra,
        headers=headers,
    )
    assert exc.message == "Invalid input"
    assert exc.context == context
    assert exc.extra == extra
    assert exc.headers == headers
    # Ensure that the quiet flag remains True
    assert exc.quiet is True
    # status_code should still be 400
    assert exc.status_code == 400


def test_badrequest_invalid_message_type():
    """Passing a non-string/non-bytes message should raise a TypeError."""
    with pytest.raises(TypeError):
        BadRequest(message=123)  # type: ignore[arg-type]
