import argparse
import sys
import io
import pytest
from httpie.cli.argparser import BaseHTTPieArgumentParser
from httpie.context import Environment
from httpie.constants import HTTP_GET

# Helper to create a minimal Environment
def make_env(stdin=None, stdout=None, stderr=None, stdin_isatty=True):
    return Environment(
        stdin=stdin or io.BytesIO(b""),
        stdout=stdout or io.StringIO(),
        stderr=stderr or io.StringIO(),
        stdin_isatty=stdin_isatty,
        stdout_encoding=sys.getdefaultencoding(),
    )

def test_parse_args_sets_debug_and_traceback():
    """Normal parsing: --debug flag sets traceback."""
    env = make_env()
    parser = BaseHTTPieArgumentParser()
    args = parser.parse_args(env, args=['--debug', HTTP_GET, 'http://example.com'])
    assert args.debug is True
    assert args.traceback is True
    assert args.request_type == HTTP_GET
    assert args.url == 'http://example.com'

def test_has_stdin_data_when_input_from_pipe():
    """Boundary: stdin not a tty and not ignored -> has_stdin_data True."""
    env = make_env(stdin=io.BytesIO(b"data"), stdin_isatty=False)
    parser = BaseHTTPieArgumentParser()
    args = parser.parse_args(env, args=[HTTP_GET, 'http://example.com'])
    assert parser.has_stdin_data is True
    assert parser.has_input_data is True

def test_unknown_option_raises_system_exit():
    """Error: unknown option triggers argparse SystemExit."""
    env = make_env()
    parser = BaseHTTPieArgumentParser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(env, args=['--unknown', HTTP_GET, 'http://example.com'])
    assert excinfo.value.code != 0
