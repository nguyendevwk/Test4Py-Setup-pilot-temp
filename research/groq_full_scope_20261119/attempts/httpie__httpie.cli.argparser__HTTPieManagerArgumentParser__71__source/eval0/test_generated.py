import argparse
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser
from httpie.exceptions import ParseError

# Test 1: Normal parsing of a simple request
def test_parse_known_args_basic():
    parser = HTTPieManagerArgumentParser()
    args, unknown = parser.parse_known_args(["GET", "http://example.com"])
    # The known args should include the method and URL
    assert args.method == "GET"
    assert args.url == "http://example.com"
    # No unknown arguments
    assert unknown == []

# Test 2: Boundary case – empty argument list should use defaults
def test_parse_known_args_empty():
    parser = HTTPieManagerArgumentParser()
    args, unknown = parser.parse_known_args([])
    # Default method should be GET
    assert args.method == "GET"
    # URL should be None when not provided
    assert args.url is None
    # No unknown arguments
    assert unknown == []

# Test 3: Error handling – missing required arguments triggers ArgumentError
def test_parse_known_args_missing_root_raises_argument_error():
    parser = HTTPieManagerArgumentParser()
    # Remove the 'root' attribute to simulate the condition in parse_known_args
    if hasattr(parser, "root"):
        delattr(parser, "root")
    # Provide an invalid argument that causes argparse to exit with code 2
    with pytest.raises(argparse.ArgumentError):
        parser.parse_known_args(["--invalid-option"])
