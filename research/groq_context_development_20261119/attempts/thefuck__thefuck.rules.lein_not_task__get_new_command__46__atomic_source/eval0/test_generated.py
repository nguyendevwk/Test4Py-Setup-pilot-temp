import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

# Helper to create a minimal command object
class DummyCommand:
    def __init__(self, output, command="lein"):
        self.output = output
        self.command = command
        self.args = []

def test_get_new_command_replaces_broken_task(monkeypatch):
    # Arrange
    output = (
        "lein 'foo' is not a task\n"
        "Did you mean this?\n"
        "lein foo\n"
        "Did you mean this?\n"
        "lein bar\n"
    )
    cmd = DummyCommand(output)

    # Monkeypatch replace_command to capture its arguments
    called = {}
    def fake_replace_command(command, broken, new_cmds):
        called['broken'] = broken
        called['new_cmds'] = new_cmds
        return f"REPLACED:{new_cmds[0]}"
    monkeypatch.setattr("thefuck.utils.replace_command", fake_replace_command)

    # Act
    result = get_new_command(cmd)

    # Assert
    assert called['broken'] == "foo"
    assert called['new_cmds'] == ["lein foo", "lein bar"]
    assert result == "REPLACED:lein foo"

def test_get_new_command_missing_broken_task_raises():
    # Arrange
    output = "Some unrelated error message"
    cmd = DummyCommand(output)

    # Act & Assert
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_no_suggestions_raises(monkeypatch):
    # Arrange
    output = "lein 'foo' is not a task\n"
    cmd = DummyCommand(output)

    # Monkeypatch get_all_matched_commands to return empty list
    monkeypatch.setattr("thefuck.utils.get_all_matched_commands", lambda o, p: [])

    # Act & Assert
    with pytest.raises(IndexError):
        get_new_command(cmd)
