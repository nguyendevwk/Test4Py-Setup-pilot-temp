import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output, command="lein"):
        self.output = output
        self.command = command

def test_get_new_command_replaces_broken_task(tmp_path):
    # Simulate a command that failed because a task was not found
    output = (
        "lein foo\n"
        "'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein bar\n"
        "  lein baz\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The new command should replace the broken task with the first suggestion
    assert new_cmd == "lein bar"

def test_get_new_command_multiple_suggestions(tmp_path):
    # Simulate multiple suggestions; the first should be used
    output = (
        "lein foo\n"
        "'foo' is not a task\n"
        "Did you mean this?\n"
        "  lein alpha\n"
        "  lein beta\n"
        "  lein gamma\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    assert new_cmd == "lein alpha"

def test_get_new_command_no_match_raises():
    # If the output does not contain the expected pattern, an IndexError should be raised
    output = (
        "lein foo\n"
        "Some unrelated error message\n"
    )
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
