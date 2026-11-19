import re
import pytest
from thefuck.rules.tsuru_not_command import get_new_command
from thefuck.utils import get_all_matched_commands, replace_command

class DummyCommand:
    def __init__(self, output):
        self.output = output

def test_get_new_command_normal(tmp_path):
    # Simulate a command output that contains a tsuru command error
    output = 'Error: tsuru: "deploy" is not a tsuru command\nSome other text'
    cmd = DummyCommand(output)
    # The function should extract "deploy" and replace it with a matched command
    new_cmd = get_new_command(cmd)
    # The new command should contain the matched command from get_all_matched_commands
    matched = get_all_matched_commands(output)
    assert matched, "Expected at least one matched command"
    # replace_command should replace the broken command with the first matched command
    expected = replace_command(cmd, "deploy", matched)
    assert new_cmd == expected, "The new command should be the result of replace_command"

def test_get_new_command_multiple_matches(tmp_path):
    # Output contains multiple tsuru command errors; only the first should be used
    output = (
        'Error: tsuru: "deploy" is not a tsuru command\n'
        'Error: tsuru: "scale" is not a tsuru command\n'
        'Some other text'
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The broken command extracted should be "deploy"
    assert "deploy" in new_cmd, "The first broken command should be used"
    # Ensure that the replacement uses the matched commands list
    matched = get_all_matched_commands(output)
    assert matched, "Expected at least one matched command"
    expected = replace_command(cmd, "deploy", matched)
    assert new_cmd == expected, "The new command should be the result of replace_command"

def test_get_new_command_no_match_raises():
    # Output does not contain the expected pattern; should raise IndexError
    output = 'Some unrelated error message'
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
