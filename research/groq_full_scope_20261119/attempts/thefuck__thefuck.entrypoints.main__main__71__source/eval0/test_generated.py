import builtins
import importlib
import sys
import types

import pytest

# Import the module under test
thefuck_main = importlib.import_module("thefuck.entrypoints.main")


@pytest.fixture(autouse=True)
def reset_sys_argv():
    """Ensure sys.argv is reset after each test."""
    original_argv = sys.argv[:]
    yield
    sys.argv = original_argv


def test_main_help(monkeypatch):
    # Prepare a dummy Parser that returns an object with help=True
    class DummyArgs:
        help = True
        version = False
        alias = False
        command = False
        shell_logger = False

    class DummyParser:
        def __init__(self):
            self.print_help_called = False

        def parse(self, argv):
            return DummyArgs()

        def print_help(self):
            self.print_help_called = True

    dummy_parser = DummyParser()
    monkeypatch.setattr(thefuck_main, "Parser", lambda: dummy_parser)

    # Run main
    thefuck_main.main()

    # Assert that print_help was called
    assert dummy_parser.print_help_called is True


def test_main_version(monkeypatch):
    # Dummy Parser returns version flag
    class DummyArgs:
        help = False
        version = True
        alias = False
        command = False
        shell_logger = False

    class DummyParser:
        def parse(self, argv):
            return DummyArgs()

    monkeypatch.setattr(thefuck_main, "Parser", lambda: DummyParser())

    # Capture logs.version call
    called = {}
    def fake_version(install_ver, py_ver, shell_info):
        called["install_ver"] = install_ver
        called["py_ver"] = py_ver
        called["shell_info"] = shell_info

    monkeypatch.setattr(thefuck_main.logs, "version", fake_version)
    monkeypatch.setattr(thefuck_main, "get_installation_version", lambda: "1.2.3")
    monkeypatch.setattr(thefuck_main.shell, "info", lambda: "bash")

    # Run main
    thefuck_main.main()

    # Assert that logs.version was called with expected arguments
    assert called["install_ver"] == "1.2.3"
    assert called["py_ver"] == sys.version.split()[0]
    assert called["shell_info"] == "bash"


def test_main_alias(monkeypatch):
    # Dummy Parser returns alias flag
    class DummyArgs:
        help = False
        version = False
        alias = True
        command = False
        shell_logger = False

    class DummyParser:
        def parse(self, argv):
            return DummyArgs()

    monkeypatch.setattr(thefuck_main, "Parser", lambda: DummyParser())

    # Capture print_alias call
    called = {}
    def fake_print_alias(args):
        called["args"] = args

    monkeypatch.setattr(thefuck_main, "print_alias", fake_print_alias)

    # Run main
    thefuck_main.main()

    # Assert that print_alias was called with the DummyArgs instance
    assert isinstance(called["args"], DummyArgs)
    assert called["args"].alias is True
