import builtins
import importlib
import os
import sys
import types

import pytest

# Import the module under test
from thefuck.entrypoints import main as main_module

# Helper to replace classes/functions in the module
def replace_in_module(module, name, new_obj):
    setattr(module, name, new_obj)


@pytest.fixture(autouse=True)
def reset_sys_argv(monkeypatch):
    """Ensure sys.argv is reset after each test."""
    original_argv = sys.argv[:]
    yield
    sys.argv = original_argv


def test_help_branch(monkeypatch, capsys):
    """When --help is passed, parser.print_help is called and nothing else."""
    # Prepare a dummy Parser that records calls
    class DummyParser:
        def __init__(self):
            self.called = False

        def parse(self, argv):
            # Simulate known_args with help=True
            return types.SimpleNamespace(help=True, version=False, alias=False,
                                        command=False, shell_logger=False)

        def print_help(self):
            self.called = True

    dummy_parser = DummyParser()
    replace_in_module(main_module, "Parser", lambda: dummy_parser)

    # Run main with --help
    sys.argv = ["thefuck", "--help"]
    main_module.main()

    # Verify that print_help was called
    assert dummy_parser.called, "Parser.print_help was not called for --help"


def test_version_branch(monkeypatch, capsys):
    """When --version is passed, logs.version is called with correct arguments."""
    # Dummy Parser
    class DummyParser:
        def parse(self, argv):
            return types.SimpleNamespace(help=False, version=True, alias=False,
                                        command=False, shell_logger=False)

        def print_help(self):
            pass

    replace_in_module(main_module, "Parser", lambda: DummyParser())

    # Capture logs.version call
    called = {}
    def dummy_version(install_ver, py_ver, shell_info):
        called["install_ver"] = install_ver
        called["py_ver"] = py_ver
        called["shell_info"] = shell_info

    replace_in_module(main_module, "logs", types.SimpleNamespace(version=dummy_version))

    # Dummy get_installation_version
    replace_in_module(main_module, "get_installation_version", lambda: "1.2.3")

    # Dummy shell.info
    class DummyShell:
        @staticmethod
        def info():
            return "bash"

    replace_in_module(main_module, "shell", DummyShell)

    # Run main with --version
    sys.argv = ["thefuck", "--version"]
    main_module.main()

    # Verify logs.version was called with expected values
    assert called["install_ver"] == "1.2.3"
    assert called["py_ver"] == sys.version.split()[0]
    assert called["shell_info"] == "bash"


def test_alias_branch(monkeypatch, capsys):
    """When --alias is passed, print_alias is called with the parsed args."""
    # Dummy Parser
    class DummyParser:
        def parse(self, argv):
            return types.SimpleNamespace(help=False, version=False, alias=True,
                                        command=False, shell_logger=False)

        def print_help(self):
            pass

    replace_in_module(main_module, "Parser", lambda: DummyParser())

    # Capture print_alias call
    called = {}
    def dummy_print_alias(args):
        called["args"] = args

    replace_in_module(main_module, "print_alias", dummy_print_alias)

    # Run main with --alias
    sys.argv = ["thefuck", "--alias"]
    main_module.main()

    # Verify print_alias was called with the parsed args
    assert called["args"].alias is True
    assert called["args"].help is False
    assert called["args"].version is False
