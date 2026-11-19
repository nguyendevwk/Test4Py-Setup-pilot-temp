import importlib
import sys
import types
import builtins

import pytest

# Import the module under test
from thefuck.entrypoints import main as main_module


@pytest.fixture
def monkeypatch_parser(monkeypatch):
    """
    Replace Parser with a dummy that records method calls and arguments.
    """
    class DummyParser:
        def __init__(self):
            self.help_called = False
            self.version_called = False
            self.alias_called = False
            self.command_called = False
            self.usage_called = False
            self.help = False
            self.version = False
            self.alias = False
            self.command = None

        def parse(self, argv):
            # Return self as known_args
            return self

        def print_help(self):
            self.help_called = True

        def print_usage(self):
            self.usage_called = True

    dummy = DummyParser()
    monkeypatch.setattr(main_module, "Parser", lambda: dummy)
    return dummy


def test_help_flag(monkeypatch_parser, capsys):
    # Simulate `thefuck --help`
    monkeypatch_parser.help = True
    sys.argv = ["thefuck", "--help"]
    main_module.main()
    # The dummy parser should have recorded a help call
    assert monkeypatch_parser.help_called
    # No other actions should be taken
    assert not monkeypatch_parser.version_called
    assert not monkeypatch_parser.alias_called
    assert not monkeypatch_parser.command_called
    assert not monkeypatch_parser.usage_called
    # Nothing should be printed to stdout
    captured = capsys.readouterr()
    assert captured.out == ""


def test_version_flag(monkeypatch_parser, capsys, monkeypatch):
    # Simulate `thefuck --version`
    monkeypatch_parser.version = True
    sys.argv = ["thefuck", "--version"]

    # Replace logs.version to capture its arguments
    called = {}
    def fake_version(install_ver, py_ver, shell_info):
        called["install_ver"] = install_ver
        called["py_ver"] = py_ver
        called["shell_info"] = shell_info

    monkeypatch.setattr(main_module.logs, "version", fake_version)
    # Also replace get_installation_version to return a known value
    monkeypatch.setattr(main_module, "get_installation_version", lambda: "1.2.3")
    # Replace shell.info to return a known string
    monkeypatch.setattr(main_module.shell, "info", lambda: "bash")

    main_module.main()

    # Verify that logs.version was called with expected arguments
    assert called["install_ver"] == "1.2.3"
    assert called["py_ver"] == sys.version.split()[0]
    assert called["shell_info"] == "bash"

    # No other parser actions should be taken
    assert not monkeypatch_parser.help_called
    assert not monkeypatch_parser.alias_called
    assert not monkeypatch_parser.command_called
    assert not monkeypatch_parser.usage_called
    captured = capsys.readouterr()
    assert captured.out == ""


def test_no_args_usage(monkeypatch_parser, capsys):
    # Simulate running without any arguments
    sys.argv = ["thefuck"]
    main_module.main()
    # The dummy parser should have recorded a usage call
    assert monkeypatch_parser.usage_called
    # No other actions should be taken
    assert not monkeypatch_parser.help_called
    assert not monkeypatch_parser.version_called
    assert not monkeypatch_parser.alias_called
    assert not monkeypatch_parser.command_called
    captured = capsys.readouterr()
    assert captured.out == ""
