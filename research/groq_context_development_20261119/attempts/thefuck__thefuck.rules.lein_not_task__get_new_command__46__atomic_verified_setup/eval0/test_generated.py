import re
import pytest
from thefuck.rules.lein_not_task import get_new_command

class DummyCommand:
    def __init__(self, command, output):
        self.command = command
        self.output = output

def test_get_new_command_replaces_with_first_suggestion():
    # Command that fails because 'foo' is not a task
    output = (
        "'foo' is not a task\n"
        "Did you mean this? foo\n"
        "Did you mean this? bar\n"
    )
    cmd = DummyCommand("lein foo", output)
    new_cmd = get_new_command(cmd)
    # The broken task 'foo' should be replaced by the first suggestion 'foo'
    assert new_cmd == "lein foo"

def test_get_new_command_uses_first_of_multiple_suggestions():
    # Two suggestions; the first should be used
    output = (
        "'baz' is not a task\n"
        "Did you mean this? qux\n"
        "Did you mean this? quux\n"
    )
    cmd = DummyCommand("lein baz", output)
    new_cmd = get_new_command(cmd)
    assert new_cmd == "lein qux"

def test_get_new_command_raises_when_no_broken_task_found():
    # Output does not contain a broken task pattern
    output = (
        "Some unrelated error message\n"
        "Did you mean this? foo\n"
    )
    cmd = DummyCommand("lein foo", output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
