import pytest
from tornado.options import options, add_parse_callback
from tornado.options import OptionParser

def test_add_parse_callback_invoked(tmp_path):
    """A callback added via add_parse_callback is invoked after parsing."""
    # Flag to verify callback execution
    executed = {"called": False}

    def my_callback():
        executed["called"] = True

    # Add callback
    add_parse_callback(my_callback)

    # Parse an empty command line (no options)
    options.parse_command_line([])

    # The callback should have been executed
    assert executed["called"] is True, "Callback was not invoked after parsing"

def test_add_parse_callback_multiple(tmp_path):
    """Adding the same callback multiple times results in multiple invocations."""
    counter = {"count": 0}

    def counter_callback():
        counter["count"] += 1

    # Add the same callback twice
    add_parse_callback(counter_callback)
    add_parse_callback(counter_callback)

    # Parse an empty command line
    options.parse_command_line([])

    # The callback should have been called twice
    assert counter["count"] == 2, f"Expected 2 invocations, got {counter['count']}"

def test_add_parse_callback_invalid_argument():
    """Providing a non-callable to add_parse_callback raises TypeError."""
    with pytest.raises(TypeError):
        add_parse_callback(42)  # non-callable argument
