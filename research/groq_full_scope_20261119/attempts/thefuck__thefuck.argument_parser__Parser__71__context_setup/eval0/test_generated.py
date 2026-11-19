import sys
import pytest
from thefuck.argument_parser import Parser
from thefuck.const import ARGUMENT_PLACEHOLDER

def test_parse_normal_arguments():
    """Parser should correctly parse standard flags and command."""
    parser = Parser()
    args = parser.parse(['thefuck', '-v', '-a', 'myalias', '-d', 'echo', 'hello'])
    assert args.version is True
    assert args.alias == 'myalias'
    assert args.debug is True
    assert args.command == ['echo', 'hello']

def test_parse_with_placeholder_moves_arguments():
    """When placeholder is present, arguments after it are moved to front."""
    parser = Parser()
    raw = ['thefuck', 'cmd', ARGUMENT_PLACEHOLDER, '-v', 'ls', '-a']
    parsed = parser.parse(raw)
    # '-v' and '-a' should be parsed as options, 'cmd' and 'ls' as command
    assert parsed.version is True
    assert parsed.alias is not None  # default alias
    assert parsed.command == ['cmd', 'ls']

def test_parse_unknown_flag_raises_systemexit():
    """Parser should exit with error on unknown option."""
    parser = Parser()
    with pytest.raises(SystemExit) as excinfo:
        parser.parse(['thefuck', '--unknown'])
    # argparse exits with code 2 on error
    assert excinfo.value.code == 2
