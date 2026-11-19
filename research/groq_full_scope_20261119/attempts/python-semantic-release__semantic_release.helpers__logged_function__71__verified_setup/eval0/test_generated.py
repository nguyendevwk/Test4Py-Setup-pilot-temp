import pytest
from semantic_release.helpers import logged_function


class DummyLogger:
    """Simple logger that records debug messages."""
    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        # Mimic logging formatting
        if args:
            msg = msg % tuple(map(str, args))
        self.messages.append(msg)


def test_logged_function_basic_return_and_logging():
    logger = DummyLogger()

    @logged_function(logger)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    # Two debug calls: one for input, one for output
    assert len(logger.messages) == 2
    # Input log contains function name and arguments
    assert logger.messages[0].startswith("add(")
    assert "2" in logger.messages[0] and "3" in logger.messages[0]
    # Output log contains function qualname and result
    assert logger.messages[1].startswith("add -> 5")


def test_logged_function_with_kwargs_and_metadata():
    logger = DummyLogger()

    @logged_function(logger)
    def greet(greeting, name="World"):
        return f"{greeting}, {name}!"

    result = greet("Hello", name="Alice")
    assert result == "Hello, Alice!"
    # Check that keyword argument is logged correctly
    assert "name=Alice" in logger.messages[0]
    # Ensure function metadata is preserved
    assert greet.__name__ == "greet"
    assert greet.__doc__ is None  # original docstring (none)


def test_logged_function_exception_handling():
    logger = DummyLogger()

    @logged_function(logger)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Only the input log should be recorded; output log is not called due to exception
    assert len(logger.messages) == 1
    assert logger.messages[0].startswith("divide(")
    assert "1" in logger.messages[0] and "0" in logger.messages[0]
