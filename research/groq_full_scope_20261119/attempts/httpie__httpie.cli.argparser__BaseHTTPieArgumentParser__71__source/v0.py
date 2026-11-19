import io
import sys
import argparse
import pytest
from httpie.cli.argparser import BaseHTTPieArgumentParser

# Minimal Environment mock used by BaseHTTPieArgumentParser
class DummyEnvironment:
    def __init__(self, stdin=None, stdin_isatty=True, stdout=None, stderr=None, stdout_encoding="utf-8"):
        self.stdin = stdin
        self.stdin_isatty = stdin_isatty
        self.stdout = stdout or io.StringIO()
        self.stderr = stderr or io.StringIO()
        self.stdout_encoding = stdout_encoding

def test_parse_args_sets_debug_and_traceback():
    env = DummyEnvironment()
    parser = BaseHTTPieArgumentParser()
    # Pass --debug flag
    ns = parser.parse_args(env, args=["--debug"])
    assert ns.debug is True
    # debug flag should enable traceback
    assert ns.traceback is True

def test_parse_args_detects_stdin_data():
    # Simulate non-tty stdin with data
    stdin = io.BytesIO(b"data")
    env = DummyEnvironment(stdin=stdin, stdin_isatty=False)
    parser = BaseHTTPieArgumentParser()
    ns = parser.parse_args(env, args=[])
    assert ns.ignore_stdin is False
    assert parser.has_stdin_data is True
    assert parser.has_input_data is True

def test_print_message_routes_to_correct_stream():
    stdout = io.StringIO()
    stderr = io.StringIO()
    env = DummyEnvironment(stdout=stdout, stderr=stderr)
    parser = BaseHTTPieArgumentParser()
    parser.env = env
    # Test message to stdout
    parser._print_message("hello stdout", file=sys.stdout)
    assert stdout.getvalue().strip() == "hello stdout"
    # Test message to stderr
    parser._print_message("hello stderr", file=sys.stderr)
    assert stderr.getvalue().strip() == "hello stderr"
    # Test message with default (None) goes to stderr
    parser._print_message("default stderr")
    assert stderr.getvalue().strip().endswith("default stderr")
