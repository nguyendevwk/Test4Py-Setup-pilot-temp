import re
import types
import pytest
from thefuck.rules.brew_install import get_new_command, _get_similar_formula, replace_argument

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula(monkeypatch):
    # Arrange
    command = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Patch the helper to return a known similar formula
    monkeypatch.setattr(
        "thefuck.rules.brew_install._get_similar_formula",
        lambda x: "bar"
    )
    # Act
    new_script = get_new_command(command)
    # Assert
    assert "foo" not in new_script
    assert "bar" in new_script
    assert new_script == "brew install bar"

def test_get_new_command_no_match_raises(monkeypatch):
    # Arrange
    command = DummyCommand(
        script="brew install foo",
        output="Some unrelated error message\n"
    )
    # Patch helper to avoid side effects
    monkeypatch.setattr(
        "thefuck.rules.brew_install._get_similar_formula",
        lambda x: "bar"
    )
    # Act & Assert
    with pytest.raises(IndexError):
        get_new_command(command)

def test_get_new_command_preserves_other_args(monkeypatch):
    # Arrange
    command = DummyCommand(
        script="brew install foo --verbose",
        output="Error: No available formula for foo\n"
    )
    monkeypatch.setattr(
        "thefuck.rules.brew_install._get_similar_formula",
        lambda x: "bar"
    )
    # Act
    new_script = get_new_command(command)
    # Assert
    assert new_script == "brew install bar --verbose"
