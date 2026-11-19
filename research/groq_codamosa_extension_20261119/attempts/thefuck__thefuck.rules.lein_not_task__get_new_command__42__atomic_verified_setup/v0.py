import re
import pytest
from types import SimpleNamespace

# Import the target function
from thefuck.rules.lein_not_task import get_new_command

# Helper to create a fake command object
def make_command(output, command_str="lein task"):
    return SimpleNamespace(output=output, command=command_str)

def test_get_new_command_replaces_first_match(monkeypatch):
    # Prepare output with two task errors and two suggestions
    output = (
        "'task1' is not a task\n"
        "'task2' is not a task\n"
        "Did you mean this?\n"
        "  lein task1\n"
        "Did you mean this?\n"
        "  lein task2\n"
    )
    cmd = make_command(output)

    # Patch replace_command to capture its arguments
    captured = {}
    def fake_replace_command(command, broken, new_cmds):
        captured['broken'] = broken
        captured['new_cmds'] = new_cmds
        return f"replaced:{broken}:{new_cmds}"
    monkeypatch.setattr("thefuck.utils.replace_command", fake_replace_command)

    result = get_new_command(cmd)

    # The broken command should be the first match
    assert captured['broken'] == "task1"
    # The new commands list should contain the two suggestions
    assert captured['new_cmds'] == ["lein task1", "lein task2"]
    # The returned value should be as defined by fake_replace_command
    assert result == "replaced:task1:['lein task1', 'lein task2']"

def test_get_new_command_raises_when_no_match():
    # Output without any "'... is not a task" pattern
    output = (
        "Some unrelated error message\n"
        "Did you mean this?\n"
        "  lein task1\n"
    )
    cmd = make_command(output)

    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_uses_first_suggestion(monkeypatch):
    # Output with one error and two suggestions
    output = (
        "'mytask' is not a task\n"
        "Did you mean this?\n"
        "  lein mytask\n"
        "Did you mean this?\n"
        "  lein mytask2\n"
    )
    cmd = make_command(output)

    # Patch replace_command to return the new command string
    def fake_replace_command(command, broken, new_cmds):
        return f"{command.command} -> {new_cmds[0]}"
    monkeypatch.setattr("thefuck.utils.replace_command", fake_replace_command)

    result = get_new_command(cmd)

    # The result should use the first suggestion
    assert result == "lein task -> lein mytask"
