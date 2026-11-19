import argparse
import sys
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser

def test_parse_known_args_success():
    """Valid arguments are parsed into a namespace without errors."""
    parser = HTTPieManagerArgumentParser()
    # Use a simple request: GET https://example.com
    args = ["GET", "https://example.com"]
    namespace, unknown = parser.parse_known_args(args)
    assert isinstance(namespace, argparse.Namespace)
    assert namespace.method == "GET"
    assert namespace.url == "https://example.com"
    assert unknown == []

def test_parse_known_args_unknown_option_raises_argument_error():
    """Unknown options trigger an ArgumentError via the overridden method."""
    parser = HTTPieManagerArgumentParser()
    # Pass an unknown flag that argparse would normally exit on
    args = ["GET", "https://example.com", "--unknown"]
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(args)
    # The exception should have a non‑empty message
    assert excinfo.value.args[1] is not None

def test_parse_known_args_system_exit_handled_as_argument_error():
    """When the parser exits with code 2 and no root attribute, an ArgumentError is raised."""
    parser = HTTPieManagerArgumentParser()
    # Provide an invalid combination that causes argparse to exit with code 2
    args = ["--help", "GET", "https://example.com"]
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(args)
    # Ensure the exception is not a SystemExit
    assert not isinstance(excinfo.value, SystemExit)
    # The message should be empty because we passed None to ArgumentError
    assert excinfo.value.args == (None, None)
