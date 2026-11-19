import builtins
import os
import sys
import types
import pytest

# Import the module under test
from thefuck.entrypoints import main as thefuck_main
from thefuck.entrypoints import main as entrypoint_module

@pytest.fixture
def monkeypatch_sys_argv(monkeypatch):
    """Reset sys.argv to a fresh list for each test."""
    monkeypatch.setattr(sys, "argv", ["thefuck"])

def test_help_flag(monkeypatch_sys_argv, tmp_path, monkeypatch):
    # Arrange: simulate --help flag
    sys.argv.append("--help")

    # Mock Parser.parse to return an object with help=True
    class DummyArgs:
        help = True
        version = False
        alias = False
        command = False
        shell_logger = False
    monkeypatch.setattr(entrypoint_module, "Parser", lambda: types.SimpleNamespace(parse=lambda _: DummyArgs()))
    # Capture print_help output
    called = {}
    def fake_print_help():
        called["help"] = True
    monkeypatch.setattr(entrypoint_module, "Parser", lambda: types.SimpleNamespace(parse=lambda _: DummyArgs(), print_help=fake_print_help))
    # Act
    entrypoint_module.main()
    # Assert
    assert called.get("help") is True

def test_alias_flag(monkeypatch_sys_argv, tmp_path, monkeypatch):
    # Arrange: simulate --alias flag
    sys.argv.append("--alias")
    # Mock Parser.parse to return an object with alias=True
    class DummyArgs:
        help = False
        version = False
        alias = True
        command = False
        shell_logger = False
    monkeypatch.setattr(entrypoint_module, "Parser", lambda: types.SimpleNamespace(parse=lambda _: DummyArgs()))
    # Capture print_alias call
    called = {}
    def fake_print_alias(args):
        called["alias_args"] = args
    monkeypatch.setattr(entrypoint_module, "print_alias", fake_print_alias)
    # Act
    entrypoint_module.main()
    # Assert
    assert called.get("alias_args") is not None
    assert called["alias_args"].alias is True

def test_command_flag(monkeypatch_sys_argv, tmp_path, monkeypatch):
    # Arrange: simulate a command argument
    sys.argv.append("echo")
    # Mock Parser.parse to return an object with command=True
    class DummyArgs:
        help = False
        version = False
        alias = False
        command = True
        shell_logger = False
    monkeypatch.setattr(entrypoint_module, "Parser", lambda: types.SimpleNamespace(parse=lambda _: DummyArgs()))
    # Capture fix_command call
    called = {}
    def fake_fix_command(args):
        called["fix_args"] = args
    monkeypatch.setattr(entrypoint_module, "fix_command", fake_fix_command)
    # Act
    entrypoint_module.main()
    # Assert
    assert called.get("fix_args") is not None
    assert called["fix_args"].command is True
