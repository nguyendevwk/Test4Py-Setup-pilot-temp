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
    """Verify that the --debug flag enables traceback."""
    env = DummyEnvironment(stdin_isatty=True)
    parser = BaseHTTPieArgumentParser()
    ns = parser.parse_args(env, args=["--debug", "GET", "http://example.com"])
    assert ns.debug is True
    assert ns.traceback is True
    # has_stdin_data should be False because stdin is a tty
    assert ns.has_stdin_data is False
    assert ns.has_input_data is False


def test_parse_args_detects_stdin_data_and_raw_input():
    """Verify that stdin data and raw input are detected correctly."""
    # stdin contains data and is not a tty
    stdin_data = io.BytesIO(b"key=value")
    env = DummyEnvironment(stdin=stdin_data, stdin_isatty=False)
    parser = BaseHTTPieArgumentParser()
    ns = parser.parse_args(env, args=["POST", "http://example.com"])
    assert ns.has_stdin_data is True
    assert ns.has_input_data is True

    # raw input via --raw flag
    env2 = DummyEnvironment(stdin_isatty=True)
    parser2 = BaseHTTPieArgumentParser()
    ns2 = parser2.parse_args(env2, args=["--raw", "rawdata", "GET", "http://example.com"])
    assert ns2.has_stdin_data is False
    assert ns2.has_input_data is True


def test_print_message_redirects_to_environment_streams():
    """Verify that _print_message writes to the correct environment streams."""
    stdout_capture = io.BytesIO()
    stderr_capture = io.BytesIO()
    env = DummyEnvironment(stdout=stdout_capture, stderr=stderr_capture, stdin_isatty=True)
    parser = BaseHTTPieArgumentParser()
    parser.env = env

    # Message to stdout
    parser._print_message("Hello stdout\n", file=sys.stdout)
    # Message to stderr
    parser._print_message("Hello stderr\n", file=sys.stderr)
    # Message with default (None) should go to stderr
    parser._print_message("Hello default\n")

    stdout_capture.seek(0)
    stderr_capture.seek(0)
    assert stdout_capture.read() == b"Hello stdout\n"
    assert stderr_capture.read() == b"Hello stderr\nHello default\n"
