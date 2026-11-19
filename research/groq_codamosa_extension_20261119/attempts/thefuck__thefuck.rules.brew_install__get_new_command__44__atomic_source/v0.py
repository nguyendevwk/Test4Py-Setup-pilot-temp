import re
import pytest
from thefuck.rules.brew_install import get_new_command
from thefuck.utils import get_closest, replace_argument
from thefuck.specific.brew import brew_available

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula():
    # Arrange: command that fails to install a non‑existent formula
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act: compute the new command using the real implementation
    new_cmd = get_new_command(cmd)

    # The new command should be the original script with the missing formula
    # replaced by a similar existing formula.
    # Determine the expected similar formula using the same helpers.
    similar = get_closest("foo", brew_available())
    expected = replace_argument(cmd.script, "foo", similar)

    # Assert: the new command matches the expected replacement
    assert new_cmd == expected
    # Assert: the new command is different from the original
    assert new_cmd != cmd.script

def test_get_new_command_raises_on_no_match():
    # Arrange: command output that does not contain the expected pattern
    cmd = DummyCommand(
        script="brew install foo",
        output="Some unrelated error message\n"
    )
    # Act & Assert: re.findall will raise IndexError because no match
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_replaces_with_closest_formula():
    # Arrange: create a command with a misspelled formula
    cmd = DummyCommand(
        script="brew install zsh",
        output="Error: No available formula for zsh\n"
    )
    # Act: get the new command
    new_cmd = get_new_command(cmd)

    # Assert: the new command should contain a formula that is close to 'zsh'
    # but not equal to the misspelled one.
    assert "zsh" not in new_cmd
    # The new command should still start with 'brew install '
    assert new_cmd.startswith("brew install ")
