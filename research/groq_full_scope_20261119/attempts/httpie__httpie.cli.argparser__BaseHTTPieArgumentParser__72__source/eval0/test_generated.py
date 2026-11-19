import io
import sys
import argparse
import pytest
from httpie.cli.argparser import BaseHTTPieArgumentParser
from httpie.context import Environment

@pytest.fixture
def env_with_stdin():
    """Environment with stdin containing data and not a tty."""
    env = Environment()
    env.stdin = io.BytesIO(b"data")
    env.stdin_isatty = False
    env.stdout = io.BytesIO()
    env.stderr = io.BytesIO()
    env.stdout_encoding = "utf-8"
    return env

@pytest.fixture
def env_without_stdin():
    """Environment with stdin empty and a tty."""
    env = Environment()
    env.stdin = io.BytesIO(b"")
    env.stdin_isatty = True
    env.stdout = io.BytesIO()
    env.stderr = io.BytesIO()
    env.stdout_encoding = "utf-8"
    return env

def test_parse_args_sets_traceback_on_debug(env_with_stdin):
    parser = BaseHTTPieArgumentParser()
    # Add a dummy debug flag
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(env_with_stdin, args=["--debug"])
    assert args.debug is True
    assert args.traceback is True  # debug flag should enable traceback

def test_parse_args_detects_stdin_data(env_with_stdin):
    parser = BaseHTTPieArgumentParser()
    # No explicit flags; parser should detect stdin data
    args = parser.parse_args(env_with_stdin, args=[])
    assert parser.has_stdin_data is True
    assert parser.has_input_data is True
    # Ensure that stdin data is not consumed by argparse
    env_with_stdin.stdin.seek(0)
    assert env_with_stdin.stdin.read() == b"data"

def test_parse_args_no_stdin_data_when_tty(env_without_stdin):
    parser = BaseHTTPieArgumentParser()
    args = parser.parse_args(env_without_stdin, args=[])
    assert parser.has_stdin_data is False
    assert parser.has_input_data is False
    # Ensure that stdin is still empty
    env_without_stdin.stdin.seek(0)
    assert env_without_stdin.stdin.read() == b""
