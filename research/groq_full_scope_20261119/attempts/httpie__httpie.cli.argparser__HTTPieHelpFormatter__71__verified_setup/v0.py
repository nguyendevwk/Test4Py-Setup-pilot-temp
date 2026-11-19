import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter


def test_split_lines_dedents_and_splits():
    formatter = HTTPieHelpFormatter()
    raw = textwrap.dedent("""
        This is a
            multi-line
        help text.
    """)
    lines = formatter._split_lines(raw, width=80)
    # The dedent should remove common indentation and strip trailing spaces
    assert lines == [
        "This is a",
        "multi-line",
        "help text.",
        "",
    ]


def test_add_usage_includes_only_positional_actions():
    parser = argparse.ArgumentParser(
        prog="testprog",
        formatter_class=HTTPieHelpFormatter,
        usage="%(prog)s [options] <url>"
    )
    # Add a positional argument
    parser.add_argument("url", help="URL to request")
    # Add an optional argument
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    # Capture the usage string
    usage = parser.format_help().splitlines()[0]
    # The usage should only show the positional argument
    assert usage == "usage: testprog <url>"


def test_add_usage_includes_invalid_option_action():
    parser = argparse.ArgumentParser(
        prog="testprog",
        formatter_class=HTTPieHelpFormatter,
        usage="%(prog)s [options] <url>"
    )
    parser.add_argument("url", help="URL to request")
    parser.add_argument("-f", "--format", choices=["json", "xml"], help="Output format")
    # Trigger an invalid option to cause ArgumentError
    with pytest.raises(SystemExit):
        parser.parse_args(["--format=invalid", "http://example.com"])
    # After the error, the help should include the invalid option action
    help_text = parser.format_help()
    # The help should contain the invalid option string
    assert "--format" in help_text
    # And the positional argument should still be present
    assert "<url>" in help_text
