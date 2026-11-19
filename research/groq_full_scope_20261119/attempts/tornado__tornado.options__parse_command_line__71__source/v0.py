import sys
import pytest
from tornado import options

def test_parse_defined_option_sets_value(tmp_path):
    # Define a simple integer option
    options.define("count", default=0, type=int, help="Number of items")
    # Parse command line with the option
    remaining = options.parse_command_line(["--count", "5"], final=True)
    # The option should be set to the parsed value
    assert options.options.count == 5
    # No remaining arguments
    assert remaining == []

def test_parse_unknown_option_with_final_false(tmp_path):
    # Ensure no option named 'foo' exists
    if hasattr(options.options, "foo"):
        delattr(options.options, "foo")
    # Parse with an unknown option, final=False should not raise
    remaining = options.parse_command_line(["--foo", "bar"], final=False)
    # The unknown option should remain in the returned list
    assert remaining == ["--foo", "bar"]
    # No attribute should be created on options
    assert not hasattr(options.options, "foo")

def test_parse_unknown_option_with_final_true_raises(tmp_path):
    # Ensure no option named 'baz' exists
    if hasattr(options.options, "baz"):
        delattr(options.options, "baz")
    # Parsing an unknown option with final=True should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        options.parse_command_line(["--baz", "qux"], final=True)
    # The exception message should mention the unknown option
    assert "--baz" in str(excinfo.value)
