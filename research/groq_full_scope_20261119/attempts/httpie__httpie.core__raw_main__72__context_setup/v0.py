import argparse
import sys
import socket
import pytest
from httpie.core import raw_main, NestedJSONSyntaxError
from httpie.context import Environment
from httpie.status import ExitStatus
import requests

# Helper parser that can be configured to raise specific exceptions
class TestParser(argparse.ArgumentParser):
    def __init__(self, *, raise_exc=None, **kwargs):
        super().__init__(**kwargs)
        self.raise_exc = raise_exc

    def parse_args(self, args=None, env=None):
        if self.raise_exc:
            raise self.raise_exc
        return argparse.Namespace()

def dummy_main_program(args, env):
    return ExitStatus.SUCCESS

def test_raw_main_debug_mode(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = TestParser()
    # Pass '--debug' to trigger debug info and early return
    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=['prog', '--debug'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.SUCCESS
    # stderr should contain debug info and environment repr
    assert 'HTTPie' in env.stderr.getvalue()
    assert 'Environment' in env.stderr.getvalue()

def test_raw_main_nested_json_error(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = TestParser(raise_exc=NestedJSONSyntaxError("bad json"))
    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=['prog', '--some', 'arg'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.ERROR
    # Error message should be written to stderr
    assert "bad json" in env.stderr.getvalue()

def test_raw_main_timeout_error(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = TestParser()
    def raising_timeout(args, env):
        raise requests.Timeout("timeout")
    exit_status = raw_main(
        parser=parser,
        main_program=raising_timeout,
        args=['prog', '--timeout', '1'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.ERROR_TIMEOUT
    # Log should contain timeout message
    assert "Request timed out" in env.log_output
