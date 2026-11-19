import pytest
from thefuck.argument_parser import Parser, ARGUMENT_PLACEHOLDER

def test_parse_basic_flags_and_command():
    """Parser should correctly parse simple flags and a command."""
    parser = Parser()
    args = parser.parse(['thefuck', '-v', '-d', 'echo', 'hello'])
    assert args.version is True
    assert args.debug is True
    assert args.command == ['echo', 'hello']

def test_parse_placeholder_moves_and_doubles():
    """Parser should move arguments after the placeholder to the front
    and add a '--' before the original command arguments."""
    parser = Parser()
    raw = ['thefuck', 'cmd', ARGUMENT_PLACEHOLDER, '-y', 'ls', '-l']
    parsed = parser.parse(raw)
    # '-y' should be parsed as a flag, 'ls -l' as command
    assert parsed.yes is True
    assert parsed.command == ['ls', '-l']

def test_parse_unknown_flag_raises_system_exit():
    """Parser should raise SystemExit when encountering an unknown flag."""
    parser = Parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(['thefuck', '--unknown'])
    # argparse exits with code 2 on error
    assert excinfo.value.code == 2
