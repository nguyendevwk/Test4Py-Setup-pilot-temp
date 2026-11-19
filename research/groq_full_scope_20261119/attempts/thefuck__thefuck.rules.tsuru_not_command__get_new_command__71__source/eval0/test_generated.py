import re
import pytest
from thefuck.rules.tsuru_not_command import get_new_command
from thefuck.utils import get_all_matched_commands, replace_command


class DummyCommand:
    def __init__(self, output, command=""):
        self.output = output
        self.command = command


def test_get_new_command_replaces_with_suggestions(monkeypatch):
    # Arrange: mock the helper functions
    broken_cmd = "deploy"
    suggestions = ["tsuru deploy", "tsuru push"]
    monkeypatch.setattr(
        "thefuck.utils.get_all_matched_commands",
        lambda output: suggestions,
    )
    monkeypatch.setattr(
        "thefuck.utils.replace_command",
        lambda cmd, broken, sugg: f"replaced:{broken}:{sugg}",
    )
    output = 'tsuru: "deploy" is not a tsuru command\nsome other text'
    cmd = DummyCommand(output=output)

    # Act
    result = get_new_command(cmd)

    # Assert
    assert result == f"replaced:{broken_cmd}:{suggestions}"


def test_get_new_command_raises_when_pattern_missing():
    # Arrange: output without the expected pattern
    output = "some unrelated error message"
    cmd = DummyCommand(output=output)

    # Act & Assert
    with pytest.raises(IndexError):
        get_new_command(cmd)


def test_get_new_command_with_empty_suggestions(monkeypatch):
    # Arrange: mock get_all_matched_commands to return empty list
    monkeypatch.setattr(
        "thefuck.utils.get_all_matched_commands",
        lambda output: [],
    )
    # Mock replace_command to simply return the broken command
    monkeypatch.setattr(
        "thefuck.utils.replace_command",
        lambda cmd, broken, sugg: f"no-suggestions:{broken}",
    )
    output = 'tsuru: "status" is not a tsuru command'
    cmd = DummyCommand(output=output)

    # Act
    result = get_new_command(cmd)

    # Assert
    assert result == "no-suggestions:status"
