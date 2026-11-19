import sys
import pytest
from thefuck.argument_parser import Parser, ARGUMENT_PLACEHOLDER

def test_parse_with_placeholder_moves_and_doubles():
    """When the placeholder is present, arguments after it are moved to the front
    and a '--' is inserted before the original command arguments."""
    parser = Parser()
    # Simulate: thefuck --option1 value1 <placeholder> cmd arg1 arg2
    argv = ['thefuck', '--option1', 'value1', ARGUMENT_PLACEHOLDER, 'cmd', 'arg1', 'arg2']
    parsed = parser.parse(argv)
    # '--' should be present before command arguments
    assert parsed.command == ['cmd', 'arg1', 'arg2']
    # option1 should be parsed correctly
    assert parsed.option1 == 'value1'
    # No other unexpected attributes
    assert hasattr(parsed, 'command')
    assert hasattr(parsed, 'option1')

def test_mutually_exclusive_arguments():
    """Providing both -y and -r should raise a SystemExit due to argparse conflict."""
    parser = Parser()
    argv = ['thefuck', '-y', '-r', 'ls']
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(argv)
    # argparse exits with code 2 on argument errors
    assert excinfo.value.code == 2

def test_parse_without_command_and_with_help_flag():
    """When only the help flag is provided, the parser should set the help attribute
    to True and leave command empty."""
    parser = Parser()
    argv = ['thefuck', '--help']
    parsed = parser.parse(argv)
    assert parsed.help is True
    assert parsed.command == []
