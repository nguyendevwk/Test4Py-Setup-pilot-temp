import types
import pytest
from semantic_release.helpers import logged_function, format_arg


class DummyLogger:
    """Simple logger that records debug calls."""
    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        # emulate logging formatting
        self.messages.append(msg % args)


def test_logged_function_logs_args_and_return_value():
    logger = DummyLogger()

    @logged_function(logger)
    def add(a, b):
        return a + b

    result = add(2, 3)

    # The function should return the correct result
    assert result == 5

    # Two debug calls should have been made: one for arguments, one for result
    assert len(logger.messages) == 2

    # First message logs the function name and arguments
    expected_args = ", ".join([format_arg(x) for x in (2, 3)])
    assert logger.messages[0] == f"add({expected_args}, )"

    # Second message logs the return value
    assert logger.messages[1] == f"add -> 5"


def test_logged_function_handles_kwargs_and_order():
    logger = DummyLogger()

    @logged_function(logger)
    def greet(greeting, name="world"):
        return f"{greeting}, {name}!"

    result = greet("Hello", name="Alice")

    assert result == "Hello, Alice!"

    # Check that kwargs are logged in the order they were passed
    assert len(logger.messages) == 2
    # Arguments message should include both positional and keyword arguments
    expected_args = ", ".join([format_arg("Hello")]) + ", " + ", ".join([f"name={format_arg('Alice')}"])
    assert logger.messages[0] == f"greet({expected_args})"

    # Return value message
    assert logger.messages[1] == "greet -> Hello, Alice!"


def test_logged_function_passes_through_exceptions():
    logger = DummyLogger()

    @logged_function(logger)
    def divide(a, b):
        return a / b

    # Division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Even though an exception was raised, the first debug call should still have been logged
    assert len(logger.messages) == 1
    assert logger.messages[0] == "divide(1, 0, )"
