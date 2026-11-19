import pytest
from sanic.exceptions import InvalidHeader
from sanic.exceptions import BadRequest


def test_invalid_header_initialization_with_message_and_headers():
    """InvalidHeader should store the message and headers correctly."""
    headers = {"X-Custom": "value", "Content-Type": "text/plain"}
    exc = InvalidHeader("Bad header", headers=headers)

    # The exception should be a subclass of BadRequest
    assert isinstance(exc, BadRequest)

    # The message should be stored as provided
    assert exc.message == "Bad header"

    # The headers should be stored exactly as passed
    assert exc.headers == headers

    # No quiet flag should be set by default
    assert exc.quiet is None

    # Context and extra should be None by default
    assert exc.context is None
    assert exc.extra is None


def test_invalid_header_quiet_flag_and_context_and_extra():
    """InvalidHeader should correctly store quiet, context, and extra arguments."""
    context = {"detail": "missing field"}
    extra = {"debug": "stacktrace"}
    exc = InvalidHeader(
        quiet=True,
        context=context,
        extra=extra,
    )

    # Quiet flag should be stored
    assert exc.quiet is True

    # Context and extra should be stored
    assert exc.context == context
    assert exc.extra == extra

    # Message should be None by default
    assert exc.message is None

    # Headers should be None by default
    assert exc.headers is None


def test_invalid_header_headers_type_validation():
    """Passing a non-dict type for headers should raise a TypeError."""
    with pytest.raises(TypeError):
        # headers must be a dict; passing a list should raise
        InvalidHeader("Bad header", headers=["not", "a", "dict"])
