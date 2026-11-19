import pytest
from thefuck.argument_parser import Parser
from thefuck.const import ARGUMENT_PLACEHOLDER

def test_parse_with_placeholder_and_command():
    parser = Parser()
    # Simulate: thefuck <placeholder> cmd arg1 arg2
    argv = ['thefuck', ARGUMENT_PLACEHOLDER, 'cmd', 'arg1', 'arg2']
    result = parser.parse(argv)
    # The command should be parsed as ['cmd', 'arg1', 'arg2']
    assert result.command == ['cmd', 'arg1', 'arg2']
    # No flags should be set
    assert not result.version
    assert not result.alias
    assert not result.shell_logger
    assert not result.enable_experimental_instant_mode
    assert not result.help
    assert not result.debug
    assert not result.force_command

def test_parse_with_mutually_exclusive_flags():
    parser = Parser()
    # Using both -y and -r should raise a SystemExit due to argparse conflict
    argv = ['thefuck', '-y', '-r', 'echo', 'test']
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(argv)
    # argparse exits with code 2 on error
    assert excinfo.value.code == 2

def test_parse_without_command_and_with_help_flag():
    parser = Parser()
    argv = ['thefuck', '--help']
    result = parser.parse(argv)
    # Help flag should be True, command list empty
    assert result.help
    assert result.command == []
    # No other flags should be set
    assert not result.version
    assert not result.alias
    assert not result.shell_logger
    assert not result.enable_experimental_instant_mode
    assert not result.debug
    assert not result.force_command
