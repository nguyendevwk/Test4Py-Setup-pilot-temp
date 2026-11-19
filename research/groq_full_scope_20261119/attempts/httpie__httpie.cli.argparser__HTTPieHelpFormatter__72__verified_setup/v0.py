import argparse
import sys
import textwrap
import pytest
from httpie.cli.argparser import HTTPieHelpFormatter


def test_usage_includes_only_positional_and_invalid_option():
    """The formatter should only display positional arguments and the
    action that caused an invalid option error."""
    parser = argparse.ArgumentParser(
        prog="httpie",
        formatter_class=HTTPieHelpFormatter,
        add_help=False
    )
    # Positional argument
    parser.add_argument("url", help="The URL to request")
    # Optional argument
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")
    # Simulate an invalid option error by calling add_argument with an invalid option string
    try:
        parser.add_argument("--invalid", help="Invalid option")
        # Force an error by parsing an unknown option
        parser.parse_args(["--invalid=foo"])
    except argparse.ArgumentError as exc:
        # The formatter will be called during the exception handling
        usage = parser.format_usage()
        # Only the positional argument should appear in the usage
        assert "url" in usage
        assert "--invalid" not in usage
        # The invalid action should be included in the usage
        assert "invalid" in usage
    else:
        pytest.fail("Expected ArgumentError was not raised")


def test_split_lines_dedents_and_preserves_blank_lines():
    """_split_lines should dedent the help text and preserve blank lines."""
    formatter = HTTPieHelpFormatter()
    raw_help = textwrap.dedent("""
        This is a help text
            with indentation.
        It has a blank line above.

        And a trailing newline.
    """)
    lines = formatter._split_lines(raw_help, width=80)
    # The first line should be the first non-indented line
    assert lines[0] == "This is a help text"
    # The second line should preserve the indentation of the second line
    assert lines[1] == "with indentation."
    # There should be an empty string representing the blank line
    assert "" in lines
    # The last line should be the trailing newline line
    assert lines[-1] == ""


def test_max_help_position_affects_alignment():
    """Changing max_help_position should affect the alignment of help text."""
    parser = argparse.ArgumentParser(
        prog="httpie",
        formatter_class=lambda *args, **kwargs: HTTPieHelpFormatter(max_help_position=20, *args, **kwargs),
        add_help=False
    )
    parser.add_argument("-a", "--alpha", help="Alpha option")
    parser.add_argument("-b", "--beta", help="Beta option")
    help_text = parser.format_help()
    # The help text should align the descriptions after 20 characters
    lines = help_text.splitlines()
    # Find the line with the alpha option
    alpha_line = next(line for line in lines if "--alpha" in line)
    # The description should start after 20 characters
    assert alpha_line[20:].lstrip().startswith("Alpha option")
