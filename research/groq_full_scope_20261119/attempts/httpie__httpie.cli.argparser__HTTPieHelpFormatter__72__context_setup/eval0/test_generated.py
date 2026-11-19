import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter

def test_usage_includes_only_positional_and_invalid_option():
    # Create a parser that will raise an ArgumentError for an invalid option
    parser = argparse.ArgumentParser(
        prog='httpie',
        formatter_class=HTTPieHelpFormatter,
        add_help=False
    )
    # Add a positional argument and an optional argument
    parser.add_argument('url', help='The URL to request')
    parser.add_argument('--style', help='Style of output')
    # Simulate passing an invalid option to trigger ArgumentError
    with pytest.raises(SystemExit):
        parser.parse_args(['--style=invalid', 'http://example.com'])
    # Capture the usage string that would be printed
    usage = parser.format_help()
    # The usage should contain only the positional argument
    assert 'usage:' in usage
    assert 'url' in usage
    assert '--style' not in usage
    # The invalid option should not appear in the usage
    assert 'invalid' not in usage

def test_split_lines_dedents_and_adds_blank_line():
    formatter = HTTPieHelpFormatter()
    # A help string with indentation and newlines
    raw_help = textwrap.dedent("""
        This is a
            multi-line
        help text.
    """)
    lines = formatter._split_lines(raw_help, width=80)
    # The first line should be the first line of the dedented text
    assert lines[0] == 'This is a'
    # The second line should be the second line without indentation
    assert lines[1] == 'multi-line'
    # The third line should be the third line
    assert lines[2] == 'help text.'
    # The last element should be an empty string due to the added blank line
    assert lines[-1] == ''

def test_max_help_position_affects_alignment():
    # Formatter with a very small max_help_position
    formatter = HTTPieHelpFormatter(max_help_position=4)
    parser = argparse.ArgumentParser(
        prog='httpie',
        formatter_class=lambda *args, **kwargs: formatter,
        add_help=False
    )
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    help_text = parser.format_help()
    # The help text should align the description after 4 spaces
    # Find the line containing the option
    for line in help_text.splitlines():
        if '--verbose' in line:
            # The description should start at column 4 (index 4)
            assert line[4:4+len('Enable verbose output')] == 'Enable verbose output'
            break
    else:
        pytest.fail('Option line not found in help text')
