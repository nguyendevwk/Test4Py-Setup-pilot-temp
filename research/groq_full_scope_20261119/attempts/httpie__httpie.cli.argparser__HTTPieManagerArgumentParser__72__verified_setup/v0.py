import argparse
import sys
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser

# Test 1: Normal parsing of a simple GET request
def test_parse_known_args_valid_get(tmp_path):
    parser = HTTPieManagerArgumentParser()
    # Simulate a minimal GET request with a URL
    args = ["http", "GET", "http://example.com"]
    namespace, unknown = parser.parse_known_args(args)
    # The parser should set the request type and URL correctly
    assert hasattr(namespace, "request_type")
    assert namespace.request_type == "GET"
    assert hasattr(namespace, "url")
    assert namespace.url == "http://example.com"
    # No unknown arguments should remain
    assert unknown == []

# Test 2: Boundary case – no arguments provided (defaults should be used)
def test_parse_known_args_no_args(tmp_path):
    parser = HTTPieManagerArgumentParser()
    # When no arguments are given, the parser should not raise and should provide defaults
    args = ["http"]
    namespace, unknown = parser.parse_known_args(args)
    # Default request type should be GET
    assert namespace.request_type == "GET"
    # URL should be None until provided
    assert namespace.url is None
    # No unknown arguments
    assert unknown == []

# Test 3: Error handling – invalid option should raise ArgumentError
def test_parse_known_args_invalid_option(tmp_path):
    parser = HTTPieManagerArgumentParser()
    # Provide an unknown option that should trigger a parsing error
    args = ["http", "--unknown-option"]
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(args)
    # The exception message should indicate the unknown option
    assert "--unknown-option" in str(excinfo.value)
