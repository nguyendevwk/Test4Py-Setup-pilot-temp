import sys
import pytest
from thefuck.argument_parser import Parser, ARGUMENT_PLACEHOLDER

def test_placeholder_moves_and_parses_command(tmp_path):
    parser = Parser()
    # Simulate command: thefuck -v <placeholder> echo hello
    argv = ['thefuck', '-v', ARGUMENT_PLACEHOLDER, 'echo', 'hello']
    parsed = parser.parse(argv)
    # '-v' flag should be True
    assert parsed.version is True
    # command should capture 'echo hello'
    assert parsed.command == ['echo', 'hello']

def test_no_arguments_parses_empty_command():
    parser = Parser()
    argv = ['thefuck']
    parsed = parser.parse(argv)
    # No flags set
    assert parsed.version is False
    assert parsed.alias is None
    assert parsed.shell_logger is None
    assert parsed.enable_experimental_instant_mode is False
    assert parsed.help is False
    assert parsed.debug is False
    assert parsed.force_command is None
    # command list should be empty
    assert parsed.command == []

def test_conflicting_arguments_raise_system_exit():
    parser = Parser()
    argv = ['thefuck', '-y', '-r', 'echo', 'hi']
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(argv)
    # argparse exits with code 2 on error
    assert excinfo.value.code == 2
