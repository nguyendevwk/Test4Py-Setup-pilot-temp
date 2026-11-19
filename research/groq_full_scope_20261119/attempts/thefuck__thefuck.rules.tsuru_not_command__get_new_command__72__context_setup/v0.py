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
    # The function should replace the broken command with a list of matched commands
    new_cmd = get_new_command(cmd)
    # The new command should contain the matched commands string
    matched = get_all_matched_commands(output)
    assert matched in new_cmd
    # The broken command should not appear in the new command
    assert 'deploy' not in new_cmd

def test_get_new_command_multiple_matches(tmp_path):
    # If multiple errors are present, only the first one is used
    output = (
        'Error: tsuru: "deploy" is not a tsuru command\n'
        'Error: tsuru: "scale" is not a tsuru command\n'
    )
    cmd = DummyCommand(output)
    new_cmd = get_new_command(cmd)
    # The replacement should use the first matched command "deploy"
    assert 'deploy' in new_cmd
    # The second command "scale" should not be used in the replacement
    assert 'scale' not in new_cmd

def test_get_new_command_no_match_raises(tmp_path):
    # When the output does not contain the expected pattern, an IndexError should be raised
    output = 'Some unrelated error message'
    cmd = DummyCommand(output)
    with pytest.raises(IndexError):
        get_new_command(cmd)
