import pytest
from sanic.exceptions import ExpectationFailed


def test_default_initialization():
    """Expect default status code, quiet flag and empty headers."""
    exc = ExpectationFailed()
    assert exc.status_code == 417
    assert exc.quiet is True
    assert exc.headers == {}
    # Default message should be the status text for 417
    assert exc.args[0] == "Expectation Failed"


def test_custom_message_and_headers():
    """Custom message and headers are preserved and quiet defaults to class value."""
    custom_headers = {"X-Custom": "value"}
    exc = ExpectationFailed("Custom error", headers=custom_headers)
    assert exc.status_code == 417
    assert exc.quiet is True  # class default
    assert exc.headers == custom_headers
    assert exc.args[0] == "Custom error"


def test_none_message_produces_status_text():
    """When message is None, the status text for the status code is used."""
    exc = ExpectationFailed(message=None)
    # The message should be the human‑readable status text for 417
    assert exc.args[0] == "Expectation Failed"
    # Ensure that the message is not empty
    assert isinstance(exc.args[0], str) and exc.args[0]
