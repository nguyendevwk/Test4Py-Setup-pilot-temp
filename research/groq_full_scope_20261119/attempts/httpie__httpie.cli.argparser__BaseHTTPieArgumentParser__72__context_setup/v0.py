import argparse
import io
import os
import sys
import tempfile
import pytest

from httpie.cli.argparser import BaseHTTPieArgumentParser
from httpie.context import Environment
from httpie.exceptions import ParseError


# Helper to create a minimal Environment instance for testing
class DummyEnvironment(Environment):
    def __init__(self, stdin=None, stdout=None, stderr=None, stdin_isatty=True):
        super().__init__()
        self.stdin = stdin or io.BytesIO()
        self.stdout = stdout or io.BytesIO()
        self.stderr = stderr or io.BytesIO()
        self.stdin_isatty = stdin_isatty
        self.stdout_encoding = "utf-8"


def test_parse_args_sets_debug_and_traceback():
    """Verify that passing --debug sets both debug and traceback flags."""
    parser = BaseHTTPieArgumentParser()
    env = DummyEnvironment(stdin_isatty=True)
    ns = parser.parse_args(env, args=["--debug", "GET", "http://example.com"])
    assert ns.debug is True
    assert ns.traceback is True
    # has_stdin_data should be False because stdin is a tty
    assert ns.has_stdin_data is False
    # has_input_data should be False as no raw data provided
    assert ns.has_input_data is False


def test_has_stdin_data_true_when_input_available():
    """Verify that has_stdin_data is True when stdin is not a tty and not ignored."""
    stdin_data = io.BytesIO(b"sample data")
    parser = BaseHTTPieArgumentParser()
    env = DummyEnvironment(stdin=stdin_data, stdin_isatty=False)
    ns = parser.parse_args(env, args=["GET", "http://example.com"])
    assert ns.has_stdin_data is True
    assert ns.has_input_data is True


def test_print_message_redirects_to_env_streams():
    """Verify that _print_message writes to the correct environment streams."""
    stdout_capture = io.BytesIO()
    stderr_capture = io.BytesIO()
    env = DummyEnvironment(stdout=stdout_capture, stderr=stderr_capture, stdin_isatty=True)

    parser = BaseHTTPieArgumentParser()
    parser.root = type("Root", (), {"env": env})()  # mimic root attribute

    # Message to stdout
    parser._print_message("Hello stdout\n", file=sys.stdout)
    # Message to stderr
    parser._print_message("Hello stderr\n", file=sys.stderr)

    stdout_capture.seek(0)
    stderr_capture.seek(0)
    assert stdout_capture.read().decode("utf-8") == "Hello stdout\n"
    assert stderr_capture.read().decode("utf-8") == "Hello stderr\n"
