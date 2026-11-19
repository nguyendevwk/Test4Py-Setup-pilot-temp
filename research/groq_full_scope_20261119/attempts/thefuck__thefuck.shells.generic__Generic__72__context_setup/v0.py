import os
import io
import pytest
from thefuck.shells.generic import Generic, ShellConfiguration
from thefuck.logs import warn
from thefuck.conf import settings

# ---------------------------------------------------------------------------

def test_alias_expansion_and_from_shell():
    """Verify that get_aliases can replace the binary name in a command."""
    class Dummy(Generic):
        def get_aliases(self):
            return {"ls": "ls --color=auto"}

    dummy = Dummy()
    # Command with alias should be expanded
    assert dummy.from_shell("ls -l") == "ls --color=auto -l"
    # Command without alias should stay unchanged
    assert dummy.from_shell("echo hello") == "echo hello"

# ---------------------------------------------------------------------------

def test_split_command_with_escaped_spaces(tmp_path):
    """split_command should correctly handle escaped spaces and preserve them."""
    dummy = Generic()
    # Create a command with an escaped space
    cmd = r'echo "Hello\ World"'
    parts = dummy.split_command(cmd)
    # The escaped space should be preserved as a single argument
    assert parts == ['echo', 'Hello World']

    # Test that a normal space splits into separate arguments
    cmd2 = "echo hello world"
    parts2 = dummy.split_command(cmd2)
    assert parts2 == ['echo', 'hello', 'world']

# ---------------------------------------------------------------------------

def test_info_handles_exception_and_warns(monkeypatch):
    """info should catch exceptions from _get_version and warn."""
    dummy = Generic()
    # Monkeypatch _get_version to raise an exception
    def bad_version():
        raise RuntimeError("boom")
    monkeypatch.setattr(dummy, "_get_version", bad_version)

    # Capture warnings
    warnings = []
    def fake_warn(msg):
        warnings.append(msg)
    monkeypatch.setattr(warn, "__call__", fake_warn)

    # Call info and verify output and warning
    result = dummy.info()
    assert result == "Generic Shell"
    assert any("Could not determine shell version" in w for w in warnings)
