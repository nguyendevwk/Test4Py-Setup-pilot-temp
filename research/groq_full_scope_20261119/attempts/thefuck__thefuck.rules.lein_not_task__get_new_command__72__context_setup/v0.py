import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output, command="lein foo"):
        self.output = output
        self.command = command

def test_get_new_command_replaces_broken_task():
    # Simulate a command output that contains a broken task and a suggestion
    output = (
        "lein: 'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein foobar\n"
        "  lein foo\n"
    )
    cmd = DummyCommand(output)
    # Mock get_all_matched_commands to return the suggestions
    def mock_get_all_matched_commands(output, keyword):
        assert keyword == "Did you mean this?"
        return ["lein foobar", "lein foo"]
    # Replace the real function with the mock
    original = get_all_matched_commands
    try:
        globals()["get_all_matched_commands"] = mock_get_all_matched_commands
        new_cmd = get_new_command(cmd)
        # The new command should be the first suggestion
        assert new_cmd.command == "lein foobar"
    finally:
        globals()["get_all_matched_commands"] = original

def test_get_new_command_multiple_broken_tasks():
    # Output contains two broken tasks; function should pick the first one
    output = (
        "lein: 'foo' is not a task\n"
        "lein: 'bar' is not a task\n"
        "Did you mean this?\n"
        "  lein foobar\n"
    )
    cmd = DummyCommand(output)
    def mock_get_all_matched_commands(output, keyword):
        return ["lein foobar"]
    original = get_all_matched_commands
    try:
        globals()["get_all_matched_commands"] = mock_get_all_matched_commands
        new_cmd = get_new_command(cmd)
        assert new_cmd.command == "lein foobar"
    finally:
        globals()["get_all_matched_commands"] = original

def test_get_new_command_no_broken_task_raises():
    # Output does not contain the expected pattern; should raise IndexError
    output = "lein: 'foo' is not a task\n"
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
