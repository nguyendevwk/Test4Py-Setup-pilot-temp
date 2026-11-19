import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter

def test_split_lines_dedents_and_adds_blank_line():
    formatter = HTTPieHelpFormatter()
    raw = "  Line one\n    Line two\n  Line three"
    lines = formatter._split_lines(raw, 80)
    # dedent removes common indentation, strip removes trailing spaces, adds two newlines
    expected = ["Line one", "Line two", "Line three", ""]
    assert lines == expected

def test_add_usage_shows_only_positional_arguments(tmp_path):
    parser = argparse.ArgumentParser(
        prog="httpie",
        usage="%(prog)s [options] URL",
        formatter_class=HTTPieHelpFormatter,
        add_help=False,
    )
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    # Capture help output
    help_text = parser.format_help()
    # Only positional argument should appear in usage line
    assert "usage:" in help_text
    assert "httpie [options] URL" in help_text
    assert "-v" not in help_text.splitlines()[0]  # option not in usage line
    # Positional argument description should be present
    assert "Target URL" in help_text

def test_add_usage_includes_invalid_option_action():
    parser = argparse.ArgumentParser(
        prog="httpie",
        usage="%(prog)s [options] URL",
        formatter_class=HTTPieHelpFormatter,
        add_help=False,
    )
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-f", "--format", help="Response format")
    # Simulate invalid option by parsing bad args
    with pytest.raises(SystemExit):
        parser.parse_args(["--format=invalid", "http://example.com"])
    # After the error, the formatter should include the invalid action in usage
    # Capture the formatter's usage by creating a new parser with the same formatter
    formatter = HTTPieHelpFormatter()
    # Manually invoke add_usage with the action that caused the error
    # The action is the one for --format
    action = next(a for a in parser._actions if a.dest == "format")
    usage_text = formatter.add_usage(
        usage="%(prog)s [options] URL",
        actions=[action],
        groups=[],
        prefix="usage:\n    "
    )
    # The usage should contain the invalid option string
    assert "--format" in usage_text
    assert "httpie [options] URL" in usage_text
