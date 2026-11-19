import types
import sys
import builtins
import importlib
import contextlib

import pytest

# Import the target function and the settings module
from thefuck.logs import how_to_configure_alias, settings, color

# Helper namedtuple for configuration details
from collections import namedtuple
ConfigDetails = namedtuple('ConfigDetails', ['content', 'path', 'reload', 'can_configure_automatically'])

def test_how_to_configure_alias_with_auto_config(caplog, capsys):
    """When configuration details are provided and automatic configuration is possible,
    the function prints the full message including the auto‑configure hint."""
    details = ConfigDetails(
        content='alias fuck="thefuck $@"',
        path='~/.bashrc',
        reload='source ~/.bashrc',
        can_configure_automatically=True
    )
    how_to_configure_alias(details)
    out, err = capsys.readouterr()
    # Basic checks for presence of key substrings
    assert 'Seems like fuck alias isn\'t configured!' in out
    assert 'Please put' in out
    assert details.content in out
    assert details.path in out
    assert details.reload in out
    assert 'Or run fuck a second time to configure it automatically.' in out
    assert 'More details - https://github.com/nvbn/thefuck#manual-installation' in out
    # Ensure no error output
    assert err == ''

def test_how_to_configure_alias_without_auto_config(caplog, capsys):
    """When configuration details are provided but automatic configuration is not possible,
    the function omits the auto‑configure hint."""
    details = ConfigDetails(
        content='alias fuck="thefuck $@"',
        path='~/.zshrc',
        reload='source ~/.zshrc',
        can_configure_automatically=False
    )
    how_to_configure_alias(details)
    out, err = capsys.readouterr()
    assert 'Or run fuck a second time to configure' not in out
    assert details.content in out
    assert details.path in out
    assert details.reload in out
    assert err == ''

def test_how_to_configure_alias_no_details_and_no_colors(caplog, capsys):
    """When no configuration details are provided and colors are disabled,
    the function prints only the minimal message without ANSI codes."""
    # Disable colors temporarily
    original_no_colors = settings.no_colors
    settings.no_colors = True
    try:
        how_to_configure_alias(None)
        out, err = capsys.readouterr()
        # The output should not contain any ANSI escape sequences
        assert '\x1b' not in out
        # Should contain the minimal message
        assert 'Seems like fuck alias isn\'t configured!' in out
        assert 'More details - https://github.com/nvbn/thefuck#manual-installation' in out
        assert err == ''
    finally:
        settings.no_colors = original_no_colors
