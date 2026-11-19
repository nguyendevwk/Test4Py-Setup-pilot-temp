import argparse
import sys
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser
from httpie.exceptions import ParseError

# Test 1: Verify that a missing required argument triggers an ArgumentError
def test_parse_known_args_missing_required():
    parser = HTTPieManagerArgumentParser(prog="httpie")
    # Assume the parser has a required positional argument named "url"
    # We simulate calling parse_known_args with no arguments
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args([])
    # The exception should have a message indicating the missing argument
    assert "the following arguments are required" in str(excinfo.value)

# Test 2: Verify that a valid URL argument is parsed correctly
def test_parse_known_args_valid_url(tmp_path):
    parser = HTTPieManagerArgumentParser(prog="httpie")
    # Provide a simple URL argument
    args, unknown = parser.parse_known_args(["https://example.com"])
    # The parsed namespace should contain the url attribute
    assert hasattr(args, "url")
    assert args.url == "https://example.com"
    # No unknown arguments should remain
    assert unknown == []

# Test 3: Verify that an invalid option raises SystemExit and is converted to ArgumentError
def test_parse_known_args_invalid_option():
    parser = HTTPieManagerArgumentParser(prog="httpie")
    # Provide an unknown option that should cause argparse to exit
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(["--unknown-option"])
    # The exception should indicate an unrecognized argument
    assert "unrecognized arguments" in str(excinfo.value)
