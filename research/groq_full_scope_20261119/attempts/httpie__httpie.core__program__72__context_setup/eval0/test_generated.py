import argparse
import io
import sys
import types
import pytest
from httpie.core import program
from httpie.status import ExitStatus

class DummyEnv:
    def __init__(self):
        self.stdout = io.BytesIO()
        self.stdout_isatty = False
        self.log_error = lambda *_, **__: None
        self.stderr = io.BytesIO()

class DummyArgs:
    def __init__(self, **kwargs):
        # provide minimal attributes used in program
        self.download = False
        self.follow = False
        self.output_file = None
        self.output_file_specified = False
        self.output_options = set()
        self.check_status = False
        self.quiet = 0
        self.headers = {}
        self.download_resume = False
        self.output_file = None
        self.output_file_specified = False
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_program_returns_success_on_no_download(tmp_path):
    """Program should return SUCCESS when no download is requested and no errors occur."""
    env = DummyEnv()
    args = DummyArgs()
    # monkeypatch collect_messages to return an empty generator to avoid real HTTP calls
    original_collect = __import__('httpie.client').collect_messages
    __import__('httpie.client').collect_messages = lambda *_, **__: iter([])
    try:
        status = program(args, env)
        assert status == ExitStatus.SUCCESS
    finally:
        __import__('httpie.client').collect_messages = original_collect

def test_program_logs_error_on_non_success_status(tmp_path):
    """When check_status is True and a non-200 status is returned, program logs an error."""
    env = DummyEnv()
    args = DummyArgs(check_status=True)
    # create a dummy message with status_code 404
    class DummyMessage:
        status_code = 404
        raw = types.SimpleNamespace(status=404, reason="Not Found")
        body = None
        headers = {}
        url = "http://example.com"
    # monkeypatch collect_messages to yield a single dummy message
    original_collect = __import__('httpie.client').collect_messages
    __import__('httpie.client').collect_messages = lambda *_, **__: iter([DummyMessage()])
    try:
        status = program(args, env)
        assert status == ExitStatus.ERROR
        # ensure error was logged
        assert b'HTTP 404 Not Found' in env.stderr.getvalue()
    finally:
        __import__('httpie.client').collect_messages = original_collect

def test_program_does_not_write_body_when_output_option_missing(tmp_path):
    """If body output option is not requested, program should not write body to stdout."""
    env = DummyEnv()
    args = DummyArgs()
    # dummy message with body
    class DummyMessage:
        status_code = 200
        raw = types.SimpleNamespace(status=200, reason="OK")
        body = b"Hello"
        headers = {}
        url = "http://example.com"
    # monkeypatch collect_messages to yield dummy message
    original_collect = __import__('httpie.client').collect_messages
    __import__('httpie.client').collect_messages = lambda *_, **__: iter([DummyMessage()])
    try:
        status = program(args, env)
        assert status == ExitStatus.SUCCESS
        # body should not be in stdout
        assert b"Hello" not in env.stdout.getvalue()
    finally:
        __import__('httpie.client').collect_messages = original_collect
