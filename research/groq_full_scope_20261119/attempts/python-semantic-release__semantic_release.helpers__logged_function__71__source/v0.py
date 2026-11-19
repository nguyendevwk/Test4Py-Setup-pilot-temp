import logging
import pytest
from semantic_release.helpers import logged_function


class ListLogger:
    """Simple logger that records debug messages in a list."""
    def __init__(self):
        self.messages = []

    def debug(self, msg, *args, **kwargs):
        # Mimic logging.Formatter behavior for % formatting
        if args:
            msg = msg % tuple(args)
        self.messages.append(msg)


def test_logged_function_normal_behavior(tmp_path):
    logger = ListLogger()

    @logged_function(logger)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    # First debug message should log function call
    assert logger.messages[0] == "add(2, 3), "
    # Second debug message should log return value
    assert logger.messages[1] == "add -> 5"


def test_logged_function_with_kwargs_and_boundary(tmp_path):
    logger = ListLogger()

    @logged_function(logger)
    def concat(prefix, *args, sep=" ", **kwargs):
        return sep.join([prefix] + list(args) + [kwargs.get("suffix", "")])

    result = concat("Hello", "world", sep="-", suffix="!")
    assert result == "Hello-world-!"
    # Check that keyword arguments are logged correctly
    assert "sep='-'" in logger.messages[0]
    assert "suffix='!'" in logger.messages[0]
    # Return value logged
    assert logger.messages[1] == "concat -> Hello-world-!"


def test_logged_function_exception_propagation(tmp_path):
    logger = ListLogger()

    @logged_function(logger)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Only the call debug message should be present; no result message
    assert len(logger.messages) == 1
    assert logger.messages[0] == "divide(1, 0), "
