import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter


def test_split_lines_dedents_and_splits():
    """_split_lines should dedent multiline help and split into lines."""
    formatter = HTTPieHelpFormatter()
    raw_help = textwrap.dedent("""
        This is a
            multiline help
        that should be dedented.
    """)
    lines = formatter._split_lines(raw_help, width=80)
    # The dedent removes leading spaces and adds two newlines at the end.
    expected = [
        "This is a",
        "multiline help",
        "that should be dedented.",
        "",
    ]
    assert lines == expected


def test_add_usage_includes_only_positional_actions():
    """add_usage should only display positional arguments."""
    parser = argparse.ArgumentParser(
        prog="testprog",
        usage="%(prog)s [options] <url>",
        formatter_class=HTTPieHelpFormatter,
    )
    # Add a positional argument and an optional one
    parser.add_argument("url", help="Target URL")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    # Capture the help output
    help_text = parser.format_help()
    # The usage line should only contain the positional argument
    assert "usage:\n    testprog <url>" in help_text
    # The optional argument should appear elsewhere in the help
    assert "--verbose" in help_text
    assert "-v" in help_text


def test_add_usage_includes_invalid_option_action():
    """When an invalid option is passed, the offending action is included in usage."""
    parser = argparse.ArgumentParser(
        prog="testprog",
        usage="%(prog)s [options] <url>",
        formatter_class=HTTPieHelpFormatter,
    )
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--style", choices=["dark", "light"], help="Style choice")
    # Simulate parsing with an invalid value for --style to trigger ArgumentError
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(["--style=invalid", "http://example.com"])
    # The exit code should be 2 (argparse error)
    assert excinfo.value.code == 2
    # Capture the help output after the error
    help_text = parser.format_help()
    # The usage line should now include the --style option
    assert "usage:\n    testprog --style <style> <url>" in help_text
    # Ensure the invalid option is mentioned in the help
    assert "--style" in help_text
