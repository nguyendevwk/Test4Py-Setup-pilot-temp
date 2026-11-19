import sys
import pytest
from thefuck.argument_parser import Parser, ARGUMENT_PLACEHOLDER

def test_parse_basic_arguments():
    """Verify that standard options are parsed correctly."""
    parser = Parser()
    args = parser.parse(['thefuck', '-v', '-d', '--shell-logger', 'log.txt', 'echo', 'hello'])
    assert args.version is True
    assert args.debug is True
    assert args.shell_logger == 'log.txt'
    assert args.command == ['echo', 'hello']

def test_placeholder_reordering_and_command_split():
    """Ensure placeholder moves following args to front and splits command."""
    parser = Parser()
    # placeholder before options
    args = parser.parse(['thefuck', ARGUMENT_PLACEHOLDER, '-y', 'ls', '-l'])
    # '-y' should be parsed as option, 'ls -l' as command
    assert args.yes is True
    assert args.command == ['ls', '-l']
    # placeholder after options
    args2 = parser.parse(['thefuck', '-d', ARGUMENT_PLACEHOLDER, 'git', 'status'])
    assert args2.debug is True
    assert args2.command == ['git', 'status']

def test_invalid_argument_raises_system_exit():
    """An unknown option should cause argparse to exit with SystemExit."""
    parser = Parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(['thefuck', '--unknown'])
    # argparse exits with code 2 on error
    assert excinfo.value.code == 2
