import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output):
        self.output = output
        self.command = "lein run"

def test_get_new_command_replaces_first_suggestion():
    # Output contains a broken task and two suggestions
    output = (
        "lein run 'foo' is not a task\n"
        "Did you mean this? bar\n"
        "Did you mean this? baz\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The broken task 'foo' should be replaced by the first suggestion 'bar'
    assert "foo" not in new_cmd
    assert "bar" in new_cmd
    assert new_cmd == replace_command(cmd, "foo", ["bar", "baz"])

def test_get_new_command_single_suggestion():
    # Output contains a broken task and a single suggestion
    output = (
        "lein run 'qux' is not a task\n"
        "Did you mean this? quux\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The broken task 'qux' should be replaced by the suggestion 'quux'
    assert "qux" not in new_cmd
    assert "quux" in new_cmd
    assert new_cmd == replace_command(cmd, "qux", ["quux"])

def test_get_new_command_no_broken_task_raises():
    # Output does not contain the expected pattern
    output = (
        "lein run 'foo' is a task\n"
        "Did you mean this? bar\n"
    )
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
