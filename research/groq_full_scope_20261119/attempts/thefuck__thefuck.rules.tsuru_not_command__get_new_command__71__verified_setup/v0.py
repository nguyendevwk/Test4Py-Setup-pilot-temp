import re
import pytest
from thefuck.rules.tsuru_not_command import get_new_command
from thefuck.utils import replace_command

class DummyCommand:
    def __init__(self, command, output):
        self.command = command
        self.output = output

def test_get_new_command_replaces_broken_command(monkeypatch):
    # Arrange: mock get_all_matched_commands to return a deterministic list
    def fake_get_all_matched_commands(output):
        return ["tsuru deploy", "tsuru status"]
    monkeypatch.setattr("thefuck.rules.tsuru_not_command.get_all_matched_commands", fake_get_all_matched_commands)

    # The broken command appears in the output
    output = 'tsuru: "deploy" is not a tsuru command\nTry: tsuru deploy\nTry: tsuru status'
    cmd = DummyCommand(command="tsuru deploy", output=output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: the new command should be the first suggestion
    assert new_cmd.command == "tsuru deploy"
    assert new_cmd.output == output

def test_get_new_command_uses_first_suggestion(monkeypatch):
    # Arrange: mock get_all_matched_commands to return multiple suggestions
    def fake_get_all_matched_commands(output):
        return ["tsuru start", "tsuru stop", "tsuru restart"]
    monkeypatch.setattr("thefuck.rules.tsuru_not_command.get_all_matched_commands", fake_get_all_matched_commands)

    output = 'tsuru: "run" is not a tsuru command\nTry: tsuru start\nTry: tsuru stop\nTry: tsuru restart'
    cmd = DummyCommand(command="tsuru run", output=output)

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: the new command should be the first suggestion
    assert new_cmd.command == "tsuru start"

def test_get_new_command_raises_when_no_match_found():
    # Arrange: output that does not contain the expected pattern
    output = 'Some unrelated error message'
    cmd = DummyCommand(command="tsuru foo", output=output)

    # Act & Assert: accessing the first element of findall should raise IndexError
    with pytest.raises(IndexError):
        get_new_command(cmd)
