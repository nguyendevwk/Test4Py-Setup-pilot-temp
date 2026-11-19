import sys
import pytest
from tornado import options

# Ensure a clean state for each test by resetting options
@pytest.fixture(autouse=True)
def reset_options():
    options._options = {}
    options._parsed = False
    yield
    options._options = {}
    options._parsed = False

def test_parse_command_line_parses_known_options_and_returns_remaining_args():
    # Define a simple integer option
    options.define("count", default=0, type=int, help="Number of items")
    # Simulate command line arguments
    args = ["--count", "5", "positional1", "positional2"]
    remaining = options.parse_command_line(args)
    # The option should be parsed and stored
    assert options.options.count == 5
    # Remaining arguments should be the positional ones
    assert remaining == ["positional1", "positional2"]

def test_parse_command_line_final_flag_stops_parsing_at_first_non_option():
    # Define a boolean option
    options.define("verbose", default=False, type=bool, help="Verbose mode")
    # Simulate command line where a non-option appears before an option
    args = ["positional1", "--verbose", "positional2"]
    remaining = options.parse_command_line(args, final=True)
    # Since final=True, parsing stops at the first non-option
    assert options.options.verbose is False  # default unchanged
    assert remaining == ["positional1", "--verbose", "positional2"]

def test_parse_command_line_unknown_option_raises_error():
    # No options defined
    args = ["--unknown", "value"]
    with pytest.raises(SystemExit) as excinfo:
        options.parse_command_line(args)
    # SystemExit should be raised with exit code 2 (usage error)
    assert excinfo.value.code == 2
