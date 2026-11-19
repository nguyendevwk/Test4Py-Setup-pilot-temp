import argparse
import io
import sys
import socket
import pytest
import requests
from httpie.core import raw_main
from httpie.context import Environment
from httpie.status import ExitStatus, http_status_to_exit_status
from httpie.models import RequestsMessageKind, OutputOptions
from httpie.output.models import ProcessingOptions
from httpie.output.writer import MESSAGE_SEPARATOR_BYTES

# Helper parser that accepts a single positional URL argument
def _make_parser():
    parser = argparse.ArgumentParser(prog="httpie")
    parser.add_argument("url")
    return parser

# Dummy main_program that simply returns SUCCESS
def _dummy_main_program(args, env):
    return ExitStatus.SUCCESS

# Test normal execution with a simple URL argument
def test_raw_main_success(tmp_path):
    env = Environment()
    env.stderr = io.StringIO()
    env.stdout = io.StringIO()
    parser = _make_parser()
    args = ["httpie", "http://example.com"]
    status = raw_main(parser, _dummy_main_program, args=args, env=env)
    assert status == ExitStatus.SUCCESS
    # stderr should be empty
    assert env.stderr.getvalue() == ""

# Test that a NestedJSONSyntaxError causes an error exit status
def test_raw_main_nested_json_error(tmp_path):
    env = Environment()
    env.stderr = io.StringIO()
    env.stdout = io.StringIO()
    parser = _make_parser()
    # Simulate parser raising NestedJSONSyntaxError
    def fake_parse_args(*_, **__):
        from httpie.cli.nested_json import NestedJSONSyntaxError
        raise NestedJSONSyntaxError("invalid json")
    parser.parse_args = fake_parse_args
    args = ["httpie", "http://example.com"]
    status = raw_main(parser, _dummy_main_program, args=args, env=env)
    assert status == ExitStatus.ERROR
    # stderr should contain the error message
    assert "invalid json" in env.stderr.getvalue()

# Test that a requests.Timeout raised by main_program results in ERROR_TIMEOUT
def test_raw_main_timeout(tmp_path):
    env = Environment()
    env.stderr = io.StringIO()
    env.stdout = io.StringIO()
    parser = _make_parser()
    def timeout_main(args, env):
        raise requests.Timeout("timeout")
    args = ["httpie", "http://example.com"]
    status = raw_main(parser, timeout_main, args=args, env=env)
    assert status == ExitStatus.ERROR_TIMEOUT
    # stderr should be empty, but log_error should have been called
    # Since log_error writes to stderr, check that it contains the timeout message
    assert "Request timed out" in env.stderr.getvalue()
