import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output, command="lein"):
        self.output = output
        self.command = command

def test_get_new_command_replaces_broken_task(tmp_path):
    # Simulate a command output that contains a broken task and a suggestion
    output = (
        "lein foo\n"
        "'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein bar\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The new command should replace the broken task with the suggested one
    assert new_cmd == "lein bar"

def test_get_new_command_no_broken_task_raises_index_error():
    # Output without the "'<task>' is not a task" pattern
    output = (
        "lein foo\n"
        "Some other error message\n"
    )
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_uses_first_suggestion(tmp_path):
    # Output with multiple suggestions; the first should be used
    output = (
        "lein foo\n"
        "'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein bar\n"
        "  lein baz\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    assert new_cmd == "lein bar"
