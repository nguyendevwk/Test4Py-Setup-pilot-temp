import pytest
from tornado import options
from tornado.options import define, options as opts

# Ensure a clean state before each test
@pytest.fixture(autouse=True)
def reset_options():
    opts.reset()
    yield
    opts.reset()


def test_parse_command_line_normal():
    # Define a simple integer option
    define("count", default=0, type=int, help="Number of items")
    # Parse a command line that sets the option and includes a positional argument
    remaining = opts.parse_command_line(["--count", "5", "positional"])
    # The option should be set correctly
    assert opts.count == 5
    # The positional argument should remain in the returned list
    assert remaining == ["positional"]


def test_parse_command_line_empty():
    # No arguments should result in an empty list and no options set
    remaining = opts.parse_command_line([])
    assert remaining == []
    # Default values should remain unchanged
    assert not hasattr(opts, "foo")  # no option defined


def test_parse_command_line_unknown_option():
    # Attempting to parse an unknown option should raise a ValueError
    with pytest.raises(ValueError) as excinfo:
        opts.parse_command_line(["--unknown"])
    # The error message should mention the unknown option
    assert "--unknown" in str(excinfo.value)
