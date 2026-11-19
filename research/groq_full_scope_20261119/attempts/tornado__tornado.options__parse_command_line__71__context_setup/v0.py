import sys
import pytest
from tornado.options import parse_command_line, options


def test_parse_command_line_remains_args():
    """When given a list of arguments, the function returns the
    unparsed arguments after processing known options."""
    # Register a dummy option to consume one argument
    options.define("foo", default="bar", type=str, help="dummy option")
    # Pass an option and an extra positional argument
    remaining = parse_command_line(["--foo", "baz", "positional"])
    # The option should be consumed and the positional argument returned
    assert remaining == ["positional"]
    # The option value should be updated
    assert options.foo == "baz"


def test_parse_command_line_uses_sys_argv(monkeypatch):
    """When args is None, parse_command_line uses sys.argv."""
    # Prepare a fake sys.argv
    fake_argv = ["script.py", "--foo", "baz", "positional"]
    monkeypatch.setattr(sys, "argv", fake_argv)
    # Ensure the option is defined
    options.define("foo", default="bar", type=str, help="dummy option")
    remaining = parse_command_line()
    # The option should be consumed and the positional argument returned
    assert remaining == ["positional"]
    assert options.foo == "baz"


def test_parse_command_line_invalid_option_raises_system_exit():
    """Passing an unknown option should cause a SystemExit."""
    # Ensure the option is not defined
    if hasattr(options, "unknown"):
        delattr(options, "unknown")
    with pytest.raises(SystemExit) as excinfo:
        parse_command_line(["--unknown", "value"])
    # SystemExit should have code 2 (typical for argparse errors)
    assert excinfo.value.code == 2
