import logging
import types
import pytest
from semantic_release.helpers import logged_function, format_arg


class DummyLogger:
    """Simple logger that records debug messages."""

    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        # Mimic logging.Formatter behaviour for % formatting
        if args:
            msg = msg % args
        self.messages.append(msg)


def test_logged_function_normal_behavior(tmp_path):
    """Verify that a normal function is wrapped and logs correctly."""
    logger = DummyLogger()

    @logged_function(logger)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    # The first debug call logs the function call
    assert logger.messages[0] == "add(2, 3, )"
    # The second debug call logs the return value
    assert logger.messages[1] == "add -> 5"


def test_logged_function_with_kwargs_and_formatting():
    """Test that keyword arguments and string formatting are handled."""
    logger = DummyLogger()

    @logged_function(logger)
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"
    # Check that string arguments are quoted in the log
    assert logger.messages[0] == "greet('Alice', greeting='Hi')"
    assert logger.messages[1] == "greet -> Hi, Alice!"


def test_logged_function_error_propagation():
    """Ensure that exceptions raised by the wrapped function are not swallowed."""
    logger = DummyLogger()

    @logged_function(logger)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    # Even though an exception occurred, the call was logged before the error
    assert logger.messages[0] == "divide(1, 0, )"
    # No result log should be present because the function did not return
    assert len(logger.messages) == 1
