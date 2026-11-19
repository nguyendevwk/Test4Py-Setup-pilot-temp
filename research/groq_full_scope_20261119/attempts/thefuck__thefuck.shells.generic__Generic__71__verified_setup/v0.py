import os
import io
import pytest
from thefuck.shells.generic import Generic
from thefuck.conf import settings

def test_alias_expansion_and_from_shell():
    """Verify that aliases are expanded correctly by from_shell."""
    class TestShell(Generic):
        def get_aliases(self):
            return {"ls": "ls --color=auto", "grep": "grep --color=auto"}

    shell = TestShell()
    # Alias present
    assert shell.from_shell("ls -l") == "ls --color=auto -l"
    # Alias not present
    assert shell.from_shell("echo hello") == "echo hello"

def test_split_command_with_escaped_spaces(tmp_path):
    """split_command should correctly handle escaped spaces and preserve quoting."""
    shell = Generic()
    # Create a command with escaped space and quoted part
    cmd = r'echo "Hello\ World" "Another\ Test"'
    parts = shell.split_command(cmd)
    # The escaped space should be treated as a literal space inside quotes
    assert parts == ['echo', 'Hello World', 'Another Test']

def test_info_handles_exception_and_warns(monkeypatch):
    """info should catch exceptions from _get_version and warn."""
    shell = Generic()
    # Monkeypatch _get_version to raise an exception
    def bad_version():
        raise RuntimeError("bad")
    monkeypatch.setattr(shell, "_get_version", bad_version)

    # Capture warnings
    warnings = []
    def fake_warn(msg):
        warnings.append(msg)
    monkeypatch.setattr(shell, "warn", fake_warn)

    result = shell.info()
    # Should contain friendly name only
    assert result == "Generic Shell"
    # Warning should have been issued
    assert any("Could not determine shell version" in w for w in warnings)
