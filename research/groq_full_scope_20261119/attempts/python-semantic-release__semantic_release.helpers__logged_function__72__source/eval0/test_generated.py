import pytest
from semantic_release.helpers import logged_function
from types import SimpleNamespace

class DummyLogger:
    def __init__(self):
        self.messages = []

    def debug(self, msg, *args):
        # mimic logging.Formatter style
        self.messages.append(msg % args)

def sample_func(a, b=2):
    return a + b

def sample_no_args():
    return "no args"

def sample_error(x):
    raise ValueError(f"bad {x}")

def test_logged_function_normal_call(tmp_path):
    logger = DummyLogger()
    decorated = logged_function(logger)(sample_func)
    result = decorated(3, b=4)
    assert result == 7
    # first debug logs input
    assert logger.messages[0] == "sample_func(3, 4)"
    # second debug logs output
    assert logger.messages[1] == "sample_func -> 7"

def test_logged_function_no_args(tmp_path):
    logger = DummyLogger()
    decorated = logged_function(logger)(sample_no_args)
    result = decorated()
    assert result == "no args"
    # input debug should show empty args
    assert logger.messages[0] == "sample_no_args()"
    # output debug
    assert logger.messages[1] == "sample_no_args -> no args"

def test_logged_function_exception(tmp_path):
    logger = DummyLogger()
    decorated = logged_function(logger)(sample_error)
    with pytest.raises(ValueError, match="bad 42"):
        decorated(42)
    # input debug should still be logged before exception
    assert logger.messages[0] == "sample_error(42)"
    # no output debug because exception occurred
    assert len(logger.messages) == 1
