import argparse
import sys
import socket
import pytest
from httpie.core import raw_main
from httpie.context import Environment
from httpie.status import ExitStatus
from httpie.models import RequestsMessageKind
from httpie.client import collect_messages
from httpie.internal.update_warnings import check_updates
from httpie.internal.daemon_runner import is_daemon_mode, run_daemon_task
from httpie.cli.constants import OUT_REQ_BODY
from httpie.cli.nested_json import NestedJSONSyntaxError
import requests

# Helper parser that simply echoes arguments
def make_parser():
    parser = argparse.ArgumentParser(prog="httpie")
    parser.add_argument("url")
    return parser

# Dummy main program that returns SUCCESS
def dummy_main(args, env):
    return ExitStatus.SUCCESS

def test_raw_main_parses_and_calls_main(monkeypatch, tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    env.config.default_options = []
    parser = make_parser()
    # Capture the arguments passed to main_program
    called = {}
    def main_program(args, env):
        called['url'] = args.url
        return ExitStatus.SUCCESS
    exit_status = raw_main(parser, main_program, args=["httpie", "https://example.com"], env=env)
    assert exit_status == ExitStatus.SUCCESS
    assert called['url'] == "https://example.com"

def test_raw_main_handles_nested_json_syntax_error(monkeypatch, tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = make_parser()
    # Monkeypatch parser.parse_args to raise NestedJSONSyntaxError
    def fake_parse_args(*_, **__):
        raise NestedJSONSyntaxError("invalid json")
    monkeypatch.setattr(parser, "parse_args", fake_parse_args)
    exit_status = raw_main(parser, dummy_main, args=["httpie", "--debug"], env=env)
    assert exit_status == ExitStatus.ERROR
    # stderr should contain the error message
    assert "invalid json" in env.stderr.getvalue()

def test_raw_main_handles_timeout(monkeypatch, tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = make_parser()
    # Main program raises Timeout
    def main_program(args, env):
        raise requests.Timeout()
    exit_status = raw_main(parser, main_program, args=["httpie", "https://example.com"], env=env)
    assert exit_status == ExitStatus.ERROR_TIMEOUT
    # log_error should record timeout message
    assert any("Request timed out" in msg for msg in env.log_messages)
