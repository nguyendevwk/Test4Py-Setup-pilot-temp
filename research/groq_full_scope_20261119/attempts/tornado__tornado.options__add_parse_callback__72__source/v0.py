import sys
import types
import pytest
from tornado import options

# Helper to reset options between tests
def reset_options():
    options._options = {}
    options._parse_callbacks = []

@pytest.fixture(autouse=True)
def cleanup():
    reset_options()
    yield
    reset_options()

def test_callback_invoked_after_parse(tmp_path):
    """The callback added via add_parse_callback is executed after parsing."""
    counter = {"called": 0}

    def callback():
        counter["called"] += 1

    options.add_parse_callback(callback)

    # Define a dummy option to trigger parsing
    options.define("dummy", default="value", type=str, help="dummy option")

    # Simulate command line parsing
    sys.argv = ["prog", "--dummy", "test"]
    options.parse_command_line()

    assert counter["called"] == 1
    assert options.get("dummy") == "test"

def test_multiple_callbacks_order(tmp_path):
    """Callbacks are called in the order they were added."""
    order = []

    def first():
        order.append("first")

    def second():
        order.append("second")

    options.add_parse_callback(first)
    options.add_parse_callback(second)

    options.define("dummy", default="value", type=str, help="dummy option")
    sys.argv = ["prog", "--dummy", "test"]
    options.parse_command_line()

    assert order == ["first", "second"]

def test_callback_called_once_per_parse(tmp_path):
    """Each callback is invoked exactly once per parse invocation."""
    counter = {"called": 0}

    def callback():
        counter["called"] += 1

    options.add_parse_callback(callback)

    options.define("dummy", default="value", type=str, help="dummy option")
    sys.argv = ["prog", "--dummy", "test"]
    options.parse_command_line()

    # Parse again with same options
    sys.argv = ["prog", "--dummy", "other"]
    options.parse_command_line()

    assert counter["called"] == 2
