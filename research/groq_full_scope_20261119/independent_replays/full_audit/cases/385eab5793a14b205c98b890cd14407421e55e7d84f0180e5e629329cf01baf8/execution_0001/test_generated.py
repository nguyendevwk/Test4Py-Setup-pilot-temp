import re
import pytest
from thefuck.rules.tsuru_not_command import get_new_command
from types import SimpleNamespace

def test_get_new_command_replaces_broken_command(monkeypatch):
    # Arrange: mock the helper functions
    def fake_get_all_matched_commands(output):
        return ["tsuru deploy", "tsuru status"]
    def fake_replace_command(command, broken, suggestions):
        # Return a string that shows what would be replaced
        return f"Replaced '{broken}' with {suggestions}"
    monkeypatch.setattr(
        "thefuck.rules.tsuru_not_command.get_all_matched_commands",
        fake_get_all_matched_commands,
    )
    monkeypatch.setattr(
        "thefuck.rules.tsuru_not_command.replace_command",
        fake_replace_command,
    )

    # Create a command object with the expected output
    cmd = SimpleNamespace(
        output='Error: tsuru: "deploy" is not a tsuru command',
        command="tsuru deploy",
    )

    # Act
    result = get_new_command(cmd)

    # Assert
    assert result == "Replaced 'deploy' with ['tsuru deploy', 'tsuru status']"

def test_get_new_command_with_multiple_quotes(monkeypatch):
    # Arrange: mock the helper functions
    def fake_get_all_matched_commands(output):
        return ["tsuru start", "tsuru stop"]
    def fake_replace_command(command, broken, suggestions):
        return f"Replaced '{broken}' with {suggestions}"
    monkeypatch.setattr(
        "thefuck.rules.tsuru_not_command.get_all_matched_commands",
        fake_get_all_matched_commands,
    )
    monkeypatch.setattr(
        "thefuck.rules.tsuru_not_command.replace_command",
        fake_replace_command,
    )

    # Command output contains two quoted strings; regex should pick the first
    cmd = SimpleNamespace(
        output='Error: tsuru: "start" is not a tsuru command and tsuru: "stop" is not a tsuru command',
        command="tsuru start",
    )

    # Act
    result = get_new_command(cmd)

    # Assert
    assert result == "Replaced 'start' with ['tsuru start', 'tsuru stop']"

def test_get_new_command_no_match_raises(monkeypatch):
    # Arrange: mock get_all_matched_commands to avoid side effects
    monkeypatch.setattr(
        "thefuck.rules.tsuru_not_command.get_all_matched_commands",
        lambda output: [],
    )
    # replace_command should not be called; we don't patch it

    # Command output does not contain the expected pattern
    cmd = SimpleNamespace(
        output='Some unrelated error message',
        command="tsuru unknown",
    )

    # Act & Assert: should raise IndexError due to regex findall[0]
    with pytest.raises(IndexError):
        get_new_command(cmd)
