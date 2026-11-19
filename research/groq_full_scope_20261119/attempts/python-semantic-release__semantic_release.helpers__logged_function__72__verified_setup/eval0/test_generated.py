import logging
import types
import pytest
from semantic_release.helpers import logged_function


class DummyLogger:
    """Simple logger that records debug messages."""

    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        # Mimic logging.Formatter behavior: format with args
        self.messages.append(msg % args if args else msg)


def test_logged_function_with_arguments_and_return_value():
    logger = DummyLogger()

    @logged_function(logger)
    def add(a, b):
        return a + b

    result = add(2, 3)

    # Verify function returns correct value
    assert result == 5

    # Verify two debug messages were logged
    assert len(logger.messages) == 2

    # First message should contain function name and formatted arguments
    assert logger.messages[0].startswith("add(")
    assert "2" in logger.messages[0]
    assert "3" in logger.messages[0]

    # Second message should contain function qualname and result
    assert logger.messages[1].startswith("add -> ")
    assert logger.messages[1].endswith("5")


def test_logged_function_with_no_arguments():
    logger = DummyLogger()

    @logged_function(logger)
    def greet():
        return "hello"

    result = greet()

    assert result == "hello"
    assert len(logger.messages) == 2
    assert logger.messages[0] == "greet(, )"
    assert logger.messages[1] == "greet -> hello"


def test_logged_function_exception_propagation_and_logging():
    logger = DummyLogger()

    @logged_function(logger)
    def fail():
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        fail()

    # Only the pre-call log should be present; post-call log is not executed
    assert len(logger.messages) == 1
    assert logger.messages[0].startswith("fail(")
