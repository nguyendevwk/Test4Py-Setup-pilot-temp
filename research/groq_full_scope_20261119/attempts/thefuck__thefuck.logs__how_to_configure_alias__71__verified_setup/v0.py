import sys
import io
import contextlib
from collections import namedtuple

import pytest

from thefuck.logs import how_to_configure_alias


def capture_output(func, *args, **kwargs):
    """Helper to capture stdout of a function."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        func(*args, **kwargs)
    return buf.getvalue()


def test_alias_without_configuration_details(capsys):
    """When no configuration details are provided, only the basic messages are printed."""
    output = capture_output(how_to_configure_alias, None)
    assert "Seems like fuck alias isn't configured!" in output
    assert "Please put" not in output
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in output
    # Ensure no extra lines
    lines = output.strip().splitlines()
    assert len(lines) == 2  # one for the first message, one for the link


def test_alias_with_configuration_details_no_auto(capsys):
    """When configuration details are provided but automatic configuration is not allowed."""
    Config = namedtuple("Config", ["content", "path", "reload", "can_configure_automatically"])
    details = Config(content="alias fuck='thefuck'", path="~/.bashrc", reload="source ~/.bashrc", can_configure_automatically=False)
    output = capture_output(how_to_configure_alias, details)
    assert "Please put alias fuck='thefuck' in your ~/.bashrc" in output
    assert "Or run fuck a second time to configure it automatically." not in output
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in output
    # Verify that the configuration line appears exactly once
    assert output.count("alias fuck='thefuck'") == 1


def test_alias_with_configuration_details_auto(capsys):
    """When configuration details allow automatic configuration, the extra instruction is printed."""
    Config = namedtuple("Config", ["content", "path", "reload", "can_configure_automatically"])
    details = Config(content="alias fuck='thefuck'", path="~/.bashrc", reload="source ~/.bashrc", can_configure_automatically=True)
    output = capture_output(how_to_configure_alias, details)
    assert "Or run fuck a second time to configure it automatically." in output
    # Ensure the automatic instruction appears only once
    assert output.count("Or run fuck a second time to configure it automatically.") == 1
