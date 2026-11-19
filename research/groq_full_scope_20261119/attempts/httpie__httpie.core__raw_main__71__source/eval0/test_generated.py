import argparse
import sys
import socket
import requests
import pytest
from httpie.core import raw_main
from httpie.context import Environment, LogLevel
from httpie.status import ExitStatus
from httpie.cli.constants import OUT_REQ_BODY
from httpie.internal.update_warnings import check_updates
from httpie.internal.daemon_runner import is_daemon_mode, run_daemon_task
from httpie.cli.nested_json import NestedJSONSyntaxError

# Helper parser that can be configured to raise an exception
class ExceptionParser(argparse.ArgumentParser):
    def __init__(self, exception=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception = exception

    def parse_args(self, args=None, namespace=None, env=None):
        if self.exception:
            raise self.exception
        return super().parse_args(args, namespace)

def dummy_main_program(args, env):
    return ExitStatus.SUCCESS

def test_raw_main_success(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    env.config.default_options = ['--output', OUT_REQ_BODY]
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    # Normal call: no exception
    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=['httpie', '--output', OUT_REQ_BODY, 'https://example.com'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.SUCCESS
    assert env.stdout.getvalue() == ''

def test_raw_main_nested_json_error(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = ExceptionParser(exception=NestedJSONSyntaxError("bad json"))
    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=['httpie', '--debug'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.ERROR
    assert "bad json" in env.stderr.getvalue()

def test_raw_main_timeout_error(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=float, default=5.0)
    def main_with_timeout(args, env):
        raise requests.Timeout()
    exit_status = raw_main(
        parser=parser,
        main_program=main_with_timeout,
        args=['httpie', '--timeout', '1'],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.ERROR_TIMEOUT
    assert "Request timed out" in env.log_buffer.getvalue()
