import pytest
from tornado import options
from tornado.options import define, parse_command_line, clear_options, add_parse_callback

# Helper to reset options between tests
@pytest.fixture(autouse=True)
def reset_options():
    clear_options()
    yield
    clear_options()


def test_single_parse_callback_invoked():
    """A single callback registered via add_parse_callback is invoked after parsing."""
    called = []

    def cb():
        called.append("called")

    add_parse_callback(cb)

    # Simulate parsing with no arguments
    parse_command_line([])

    assert called == ["called"], "Callback should be called once after parsing"


def test_multiple_callbacks_order():
    """Callbacks are invoked in the order they were added."""
    order = []

    def first():
        order.append("first")

    def second():
        order.append("second")

    add_parse_callback(first)
    add_parse_callback(second)

    parse_command_line([])

    assert order == ["first", "second"], "Callbacks should run in registration order"


def test_callback_can_modify_option():
    """A callback can modify option values after parsing."""
    # Define an option with a default value
    define("test_opt", default="original", type=str)

    def modify():
        # Change the option value during callback
        options.test_opt = "modified"

    add_parse_callback(modify)

    parse_command_line([])

    assert options.test_opt == "modified", "Callback should be able to modify option values"
