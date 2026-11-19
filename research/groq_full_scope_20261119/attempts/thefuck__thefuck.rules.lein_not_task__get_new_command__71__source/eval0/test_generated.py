import re
import pytest
from thefuck.rules.lein_not_task import get_new_command

class DummyCommand:
    def __init__(self, command, output):
        self.command = command
        self.output = output

def test_get_new_command_replaces_first_suggestion():
    # Arrange: command output contains a broken task and two suggestions
    output = (
        "lein: 'mytask' is not a task\n"
        "Did you mean this?\n"
        "  lein mytask\n"
        "Did you mean this?\n"
        "  lein mytask2\n"
    )
    cmd = DummyCommand("lein mytask", output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: the broken task is replaced by the first suggestion
    assert "mytask" not in new_cmd.command
    assert "lein mytask" in new_cmd.command
    assert new_cmd.command != cmd.command

def test_get_new_command_raises_when_no_broken_task():
    # Arrange: output does not contain the expected pattern
    output = "Some unrelated error message"
    cmd = DummyCommand("lein mytask", output)

    # Act & Assert: IndexError is raised because re.findall returns empty list
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_uses_only_first_match_of_broken_task():
    # Arrange: output contains two broken task patterns; only the first should be used
    output = (
        "lein: 'first' is not a task\n"
        "lein: 'second' is not a task\n"
        "Did you mean this?\n"
        "  lein first\n"
    )
    cmd = DummyCommand("lein first", output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: only the first broken task ('first') is replaced
    assert "first" not in new_cmd.command
    assert "second" in new_cmd.command
    assert "lein first" in new_cmd.command
