import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, command, output):
        self.command = command
        self.output = output

def test_get_new_command_replaces_broken_task():
    # Simulate a lein output that reports a missing task and suggests a correction
    output = (
        "lein: 'mytask' is not a task\n"
        "Did you mean this? lein mytask\n"
    )
    cmd = DummyCommand("lein mytask", output)
    new_cmd = get_new_command(cmd)
    # The new command should contain the suggested task name
    assert "mytask" in new_cmd.command
    # The broken task string should no longer be present
    assert "'mytask'" not in new_cmd.command

def test_get_new_command_multiple_suggestions():
    # Simulate output with multiple suggestions; replace_command should pick the first
    output = (
        "lein: 'mytask' is not a task\n"
        "Did you mean this? lein mytask1\n"
        "Did you mean this? lein mytask2\n"
    )
    cmd = DummyCommand("lein mytask", output)
    new_cmd = get_new_command(cmd)
    # The new command should use the first suggestion
    assert new_cmd.command == "lein mytask1"

def test_get_new_command_no_match_raises_index_error():
    # Output that does not contain the expected pattern should raise IndexError
    output = "lein: unknown error occurred"
    cmd = DummyCommand("lein mytask", output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
