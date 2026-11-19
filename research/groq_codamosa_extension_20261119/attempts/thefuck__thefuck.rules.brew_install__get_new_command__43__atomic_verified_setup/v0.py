import re
import pytest
from thefuck.rules.brew_install import get_new_command, _get_similar_formula
from thefuck.utils import replace_argument

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula(tmp_path):
    # Arrange: create a command that simulates a brew install error
    script = "brew install foobar"
    output = "Error: No available formula for foobar\n"
    cmd = DummyCommand(script, output)

    # Act: get the new command suggested by the rule
    new_cmd = get_new_command(cmd)

    # Assert: the new command should replace 'foobar' with a similar formula
    # _get_similar_formula should return a string that is not the same as the original
    similar = _get_similar_formula("foobar")
    assert similar != "foobar"
    assert new_cmd == replace_argument(script, "foobar", similar)

def test_get_new_command_raises_on_no_match():
    # Arrange: command output that does not contain the expected error pattern
    script = "brew install nonexistent"
    output = "Some unrelated error message\n"
    cmd = DummyCommand(script, output)

    # Act & Assert: accessing the first element of the regex result raises IndexError
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_handles_multiple_errors():
    # Arrange: output containing multiple error lines; the regex should pick the first
    script = "brew install foo bar"
    output = (
        "Error: No available formula for foo\n"
        "Error: No available formula for bar\n"
    )
    cmd = DummyCommand(script, output)

    # Act: get the new command
    new_cmd = get_new_command(cmd)

    # Assert: only the first formula 'foo' is replaced
    similar = _get_similar_formula("foo")
    assert new_cmd == replace_argument(script, "foo", similar)
    assert "bar" in new_cmd  # bar remains unchanged
