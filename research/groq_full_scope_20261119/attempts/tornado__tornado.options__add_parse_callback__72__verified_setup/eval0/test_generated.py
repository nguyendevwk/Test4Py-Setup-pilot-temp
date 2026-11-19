import pytest
from tornado import options
from tornado.options import add_parse_callback, parse_command_line, clear_options, define, options as opts


def test_callback_invoked_after_parsing(tmp_path):
    """The callback registered via add_parse_callback should be called after parsing."""
    # Ensure a clean state
    clear_options()
    # Define a dummy option
    define("dummy", default=42, type=int, help="dummy option")
    # Flag to verify callback execution
    executed = {"called": False}

    def callback():
        executed["called"] = True

    add_parse_callback(callback)
    # Parse an empty command line (no args)
    parse_command_line([])
    assert executed["called"] is True, "Callback was not invoked after parsing"


def test_multiple_callbacks_order(tmp_path):
    """Multiple callbacks should be invoked in the order they were added."""
    clear_options()
    order = []

    def first():
        order.append("first")

    def second():
        order.append("second")

    add_parse_callback(first)
    add_parse_callback(second)
    parse_command_line([])
    assert order == ["first", "second"], f"Callbacks executed in wrong order: {order}"


def test_invalid_callback_type_raises():
    """add_parse_callback should raise TypeError when given a non-callable."""
    clear_options()
    with pytest.raises(TypeError):
        add_parse_callback(123)  # non-callable argument
