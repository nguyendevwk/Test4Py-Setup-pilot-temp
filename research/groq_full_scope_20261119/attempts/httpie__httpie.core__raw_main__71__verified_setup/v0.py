import argparse
import sys
import socket
import requests
import pytest
from httpie.core import raw_main
from httpie.context import Environment, LogLevel
from httpie.status import ExitStatus
from httpie.internal.update_warnings import check_updates
from httpie.internal.daemon_runner import is_daemon_mode, run_daemon_task
from httpie.cli.constants import OUT_REQ_BODY
from httpie.cli.nested_json import NestedJSONSyntaxError
from httpie.plugins.registry import plugin_manager

# ----------------------------------------------------------------------
# Helper parser that can be configured to raise specific exceptions
# ----------------------------------------------------------------------
class TestParser(argparse.ArgumentParser):
    def __init__(self, *, raise_exc=None, **kwargs):
        super().__init__(**kwargs)
        self.raise_exc = raise_exc

    def parse_args(self, args=None, env=None):
        if self.raise_exc:
            raise self.raise_exc
        return super().parse_args(args, env=env)

# ----------------------------------------------------------------------
# Dummy main_program that simply returns SUCCESS
# ----------------------------------------------------------------------
def dummy_main_program(args, env):
    return ExitStatus.SUCCESS

# ----------------------------------------------------------------------
# Test 1: Normal execution path
# ----------------------------------------------------------------------
def test_raw_main_success(tmp_path):
    env = Environment()
    env.config.plugins_dir = tmp_path
    env.config.default_options = []
    env.log_level = LogLevel.INFO
    env.stderr = sys.stderr

    parser = TestParser()
    parser.add_argument("url")

    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=["httpie", "http://example.com"],
        env=env,
        use_default_options=True,
    )
    assert exit_status == ExitStatus.SUCCESS

# ----------------------------------------------------------------------
# Test 2: NestedJSONSyntaxError during argument parsing
# ----------------------------------------------------------------------
def test_raw_main_nested_json_error(tmp_path, capsys):
    env = Environment()
    env.config.plugins_dir = tmp_path
    env.stderr = sys.stderr

    parser = TestParser(raise_exc=NestedJSONSyntaxError("bad json"))
    parser.add_argument("url")

    exit_status = raw_main(
        parser=parser,
        main_program=dummy_main_program,
        args=["httpie", "http://example.com"],
        env=env,
        use_default_options=False,
    )
    captured = capsys.readouterr()
    assert "bad json" in captured.err
    assert exit_status == ExitStatus.ERROR

# ----------------------------------------------------------------------
# Test 3: requests.Timeout raised by main_program
# ----------------------------------------------------------------------
def test_raw_main_timeout(tmp_path, caplog):
    env = Environment()
    env.config.plugins_dir = tmp_path
    env.log_level = LogLevel.INFO
    env.stderr = sys.stderr

    def timeout_main(args, env):
        raise requests.Timeout("timeout")

    parser = TestParser()
    parser.add_argument("url")

    exit_status = raw_main(
        parser=parser,
        main_program=timeout_main,
        args=["httpie", "http://example.com"],
        env=env,
        use_default_options=False,
    )
    assert exit_status == ExitStatus.ERROR_TIMEOUT
    assert any("Request timed out" in rec.message for rec in caplog.records)
