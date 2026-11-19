import pytest
from sanic.exceptions import BadRequest
from sanic.helpers import STATUS_CODES


def test_default_message_and_status():
    """BadRequest without a message should use the default status text."""
    exc = BadRequest()
    # The default message should be the status code's description
    assert exc.message == STATUS_CODES[400]
    # Status code must be 400
    assert exc.status_code == 400
    # quiet flag should be True by default
    assert exc.quiet is True


def test_custom_headers_and_context():
    """Custom headers and context should be stored correctly."""
    headers = {"X-Custom": "value"}
    context = {"detail": "invalid input"}
    exc = BadRequest(message="Bad data", headers=headers, context=context)
    # Headers should be accessible via the headers attribute
    assert exc.headers == headers
    # Context should be stored in the context attribute
    assert exc.context == context
    # The message should be the one provided
    assert exc.message == "Bad data"


def test_status_code_and_quiet_attributes():
    """Ensure that status_code and quiet attributes are class-level constants."""
    # The class attribute status_code should be 400
    assert BadRequest.status_code == 400
    # The class attribute quiet should be True
    assert BadRequest.quiet is True
    # Instances should inherit these values
    exc = BadRequest()
    assert exc.status_code == 400
    assert exc.quiet is True
