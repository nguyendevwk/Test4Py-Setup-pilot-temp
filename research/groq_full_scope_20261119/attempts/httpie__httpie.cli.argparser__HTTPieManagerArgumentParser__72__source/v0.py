import argparse
import pytest
from httpie.cli.argparser import HTTPieManagerArgumentParser

def test_parse_known_args_success(tmp_path):
    """Verify that parse_known_args returns a namespace and unknown args."""
    parser = HTTPieManagerArgumentParser()
    # Provide a simple URL argument that should be parsed as a request item
    args = ["http://example.com"]
    namespace, unknown = parser.parse_known_args(args)
    # The namespace should contain the parsed URL under the 'url' attribute
    assert hasattr(namespace, "url")
    assert namespace.url == "http://example.com"
    # No unknown arguments should remain
    assert unknown == []

def test_parse_known_args_error_without_root(tmp_path):
    """When no root attribute and a parsing error occurs, an ArgumentError should be raised."""
    parser = HTTPieManagerArgumentParser()
    # Pass an invalid option that triggers a SystemExit with code 2
    args = ["--invalid-option"]
    with pytest.raises(argparse.ArgumentError) as excinfo:
        parser.parse_known_args(args)
    # The exception should have no message (None, None)
    assert excinfo.value.args == (None, None)

def test_parse_known_args_error_with_root(tmp_path):
    """If the parser has a 'root' attribute, SystemExit should propagate unchanged."""
    parser = HTTPieManagerArgumentParser()
    # Simulate the presence of a root attribute
    parser.root = object()
    args = ["--invalid-option"]
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_known_args(args)
    # The SystemExit code should be 2 (argument parsing error)
    assert excinfo.value.code == 2
