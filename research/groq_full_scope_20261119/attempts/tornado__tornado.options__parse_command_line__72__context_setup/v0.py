import pytest
from tornado.options import parse_command_line, options

def test_parse_known_option_removes_it(tmp_path):
    # Define a temporary option to avoid side effects on global state
    options.define("test_option", default="default", type=str, help="test")
    # Pass the option on the command line
    remaining = parse_command_line(["--test_option", "value"])
    # The option should be parsed and removed from the remaining list
    assert remaining == []
    # The option value should be set correctly
    assert options.test_option == "value"

def test_parse_no_args_returns_empty_list():
    # When no arguments are supplied, parse_command_line should return an empty list
    remaining = parse_command_line([])
    assert remaining == []

def test_parse_unknown_option_raises_value_error():
    # Passing an unknown option should raise a ValueError
    with pytest.raises(ValueError) as excinfo:
        parse_command_line(["--unknown_option", "foo"])
    assert "unknown option" in str(excinfo.value).lower()
