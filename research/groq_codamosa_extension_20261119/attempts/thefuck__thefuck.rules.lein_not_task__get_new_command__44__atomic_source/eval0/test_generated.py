import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output, command="lein"):
        self.output = output
        self.command = command

def test_get_new_command_single_suggestion():
    # Output contains a single suggestion after the error message
    output = (
        "lein 'foo' is not a task\n"
        "Did you mean this?\n"
        "lein foo\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The new command should be the suggested one
    assert new_cmd == "lein foo"

def test_get_new_command_multiple_suggestions():
    # Output contains multiple suggestions; replace_command should pick the first
    output = (
        "lein 'bar' is not a task\n"
        "Did you mean this?\n"
        "lein bar\n"
        "lein bar2\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The new command should be the first suggestion
    assert new_cmd == "lein bar"

def test_get_new_command_no_match_raises():
    # Output missing the expected pattern should raise an IndexError
    output = (
        "lein 'baz' is not a task\n"
        "Some unrelated output\n"
    )
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
