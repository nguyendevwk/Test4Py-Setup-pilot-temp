import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter


def test_split_lines_dedents_and_preserves_blank_lines(tmp_path):
    """_split_lines should dedent multiline help and keep blank lines."""
    formatter = HTTPieHelpFormatter()
    raw_help = textwrap.dedent("""
        This is a test help text.
            It has indentation.
        And a blank line above.

        End of help.
    """)
    lines = formatter._split_lines(raw_help, width=80)
    # The first line should be the first non-indented line
    assert lines[0] == "This is a test help text."
    # The second line should be dedented
    assert lines[1] == "It has indentation."
    # The third line should be the blank line that was present
    assert lines[2] == ""
    # The last line should be the final line
    assert lines[-1] == "End of help."


def test_add_usage_shows_only_positional_arguments(tmp_path):
    """add_usage should only display positional arguments in the usage string."""
    parser = argparse.ArgumentParser(
        prog="testprog",
        formatter_class=HTTPieHelpFormatter,
        add_help=False,
    )
    # Add a positional argument and an optional one
    parser.add_argument("positional", help="positional argument")
    parser.add_argument("-o", "--optional", help="optional argument")
    # Capture the usage string
    usage_lines = []
    def fake_print(*args, **kwargs):
        usage_lines.append(" ".join(args))
    # Temporarily replace sys.stdout.write
    original_write = sys.stdout.write
    sys.stdout.write = fake_print
    try:
        parser.print_usage()
    finally:
        sys.stdout.write = original_write
    # The usage should contain only the positional argument
    usage_text = " ".join(usage_lines)
    assert "positional" in usage_text
    assert "-o" not in usage_text
    assert "--optional" not in usage_text


def test_add_usage_includes_action_on_invalid_option(tmp_path):
    """When an invalid option is passed, add_usage should include the offending action."""
    parser = argparse.ArgumentParser(
        prog="testprog",
        formatter_class=HTTPieHelpFormatter,
        add_help=False,
    )
    parser.add_argument("positional", help="positional argument")
    parser.add_argument("-f", "--foo", help="foo option")
    # Simulate parsing with an invalid option to trigger ArgumentError
    with pytest.raises(SystemExit):
        parser.parse_args(["--invalid"])
    # Capture the usage string after the error
    usage_lines = []
    def fake_print(*args, **kwargs):
        usage_lines.append(" ".join(args))
    original_write = sys.stdout.write
    sys.stdout.write = fake_print
    try:
        parser.print_usage()
    finally:
        sys.stdout.write = original_write
    usage_text = " ".join(usage_lines)
    # The usage should now include the invalid option action
    assert "--invalid" in usage_text
    # And still only show positional arguments
    assert "positional" in usage_text
    assert "-f" not in usage_text
