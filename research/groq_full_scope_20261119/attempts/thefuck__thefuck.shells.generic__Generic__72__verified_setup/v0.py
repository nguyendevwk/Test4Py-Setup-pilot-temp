import os
import io
import shlex
import pytest
from thefuck.shells.generic import Generic
from thefuck.conf import settings

class DummyGeneric(Generic):
    """Subclass to override protected methods for testing."""
    def __init__(self, history_file, history_limit=None):
        super().__init__()
        self._history_file = history_file
        if history_limit is not None:
            settings.history_limit = history_limit

    def _get_history_file_name(self):
        return self._history_file

    def _get_version(self):
        return "1.2.3"

def test_alias_expansion(tmp_path):
    """Test that _expand_aliases replaces known aliases."""
    alias_map = {"ls": "ls --color=auto"}
    g = Generic()
    g.get_aliases = lambda: alias_map
    # Alias present
    assert g._expand_aliases("ls -l") == "ls --color=auto -l"
    # Alias absent
    assert g._expand_aliases("echo hello") == "echo hello"

def test_split_command_with_escaped_spaces(tmp_path):
    """Test split_command correctly handles escaped spaces."""
    g = Generic()
    # Command with escaped space
    cmd = r'echo "Hello\ World"'
    parts = g.split_command(cmd)
    # shlex should interpret escaped space as part of argument
    assert parts == ['echo', 'Hello World']

def test_history_and_info(tmp_path):
    """Test get_history respects history_limit and info uses overridden version."""
    # Create a temporary history file with 5 lines
    hist_file = tmp_path / "history.txt"
    hist_file.write_text("cmd1\ncmd2\ncmd3\ncmd4\ncmd5\n")
    # Set history_limit to 3
    g = DummyGeneric(str(hist_file), history_limit=3)
    history = g.get_history()
    # Should return last 3 commands
    assert history == ["cmd3", "cmd4", "cmd5"]
    # Test info method uses overridden _get_version
    assert g.info() == "Generic Shell 1.2.3"
