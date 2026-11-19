import argparse
import sys
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser

# Test 1: Normal parsing of a simple request
def test_parse_known_args_basic():
    parser = HTTPieManagerArgumentParser()
    # Simulate a simple GET request to example.com
    args, unknown = parser.parse_known_args(["GET", "https://example.com"])
    # The parsed namespace should contain the method and URL
    assert hasattr(args, "method") and args.method == "GET"
    assert hasattr(args, "url") and args.url == "https://example.com"
    # No unknown arguments should remain
    assert unknown == []

# Test 2: Argument error triggers SystemExit and is converted to ArgumentError
def test_parse_known_args_invalid_argument_raises_argument_error():
    parser = HTTPieManagerArgumentParser()
    # Pass an invalid flag that the parser does not recognize
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(["--unknown-flag"])
    # The exception should have a message indicating the unknown argument
    assert "unrecognized arguments" in str(excinfo.value)

# Test 3: When the parser has a 'root' attribute, SystemExit is re‑raised unchanged
def test_parse_known_args_with_root_attribute():
    parser = HTTPieManagerArgumentParser()
    # Attach a dummy root attribute to simulate a different parser state
    parser.root = object()
    # Passing an invalid flag should still raise SystemExit with code 2
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_known_args(["--invalid"])
    assert excinfo.value.code == 2
