import re
import pytest
from thefuck.rules.brew_install import get_new_command
from thefuck.utils import replace_argument

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula(tmp_path):
    # Arrange: create a command that triggers the rule
    script = "brew install foobar"
    # Use a formula name that is unlikely to exist but has a close match in brew
    output = "Error: No available formula for foobar"
    cmd = DummyCommand(script, output)

    # Act: get the new command
    new_cmd = get_new_command(cmd)

    # Assert: the new command should replace 'foobar' with a similar existing formula
    # The replacement should not contain the original 'foobar'
    assert "foobar" not in new_cmd
    # The new command should still start with 'brew install'
    assert new_cmd.startswith("brew install")
    # The new command should be different from the original
    assert new_cmd != script

def test_get_new_command_no_match_raises_index_error():
    # Arrange: command output without the expected pattern
    script = "brew install nonexistent"
    output = "Some unrelated error message"
    cmd = DummyCommand(script, output)

    # Act & Assert: accessing the first match should raise IndexError
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_multiple_matches_returns_first(tmp_path):
    # Arrange: output containing two error messages; regex should pick the first
    script = "brew install foo bar"
    output = (
        "Error: No available formula for foo\n"
        "Error: No available formula for bar\n"
    )
    cmd = DummyCommand(script, output)

    # Act: get the new command
    new_cmd = get_new_command(cmd)

    # Assert: only the first formula 'foo' should be replaced
    assert "foo" not in new_cmd
    assert "bar" in new_cmd
    # Ensure the replacement is a valid formula (not the original)
    assert new_cmd != script
