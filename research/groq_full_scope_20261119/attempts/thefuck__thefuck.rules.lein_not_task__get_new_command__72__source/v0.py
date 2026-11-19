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
        "Did you mean this? lein mytask2\n"
    )
    cmd = DummyCommand("lein mytask", output)
    new_cmd = get_new_command(cmd)
    # The broken task should be replaced by the first suggestion
    assert new_cmd.command == "lein mytask"

def test_get_new_command_raises_when_no_match():
    # Output that does not contain the expected pattern
    output = "lein: 'mytask' is not a task\n"
    cmd = DummyCommand("lein mytask", output)
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_uses_first_suggestion_when_multiple():
    # Multiple suggestions are present; the first should be used
    output = (
        "lein: 'mytask' is not a task\n"
        "Did you mean this? lein mytask1\n"
        "Did you mean this? lein mytask2\n"
    )
    cmd = DummyCommand("lein mytask", output)
    new_cmd = get_new_command(cmd)
    assert new_cmd.command == "lein mytask1"
