import re
import pytest
from thefuck.rules.lein_not_task import get_new_command
from thefuck.utils import replace_command, get_all_matched_commands

class DummyCommand:
    def __init__(self, output, command="lein foo"):
        self.output = output
        self.command = command

def test_get_new_command_replaces_broken_task():
    # Output contains a broken task and a suggestion
    output = (
        "lein foo is not a task\n"
        "Did you mean this? lein bar\n"
    )
    cmd = DummyCommand(output)
    # get_all_matched_commands will return ['lein bar']
    new_cmd = get_new_command(cmd)
    # replace_command should replace 'foo' with 'lein bar'
    assert new_cmd == "lein bar"

def test_get_new_command_multiple_suggestions():
    # Output contains multiple suggestions; replace_command should pick the first
    output = (
        "lein baz is not a task\n"
        "Did you mean this? lein qux\n"
        "Did you mean this? lein quux\n"
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # Expect the first suggestion to be used
    assert new_cmd == "lein qux"

def test_get_new_command_no_match_raises():
    # Output does not contain the expected pattern; re.findall will fail
    output = "lein foo is not a task but no suggestions"
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
