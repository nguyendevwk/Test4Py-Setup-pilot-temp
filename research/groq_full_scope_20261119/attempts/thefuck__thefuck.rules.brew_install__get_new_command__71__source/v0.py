import re
import pytest
from thefuck.rules import brew_install
from thefuck.utils import replace_argument

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula(monkeypatch):
    # Arrange
    dummy = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Patch the helper to return a known replacement
    monkeypatch.setattr(brew_install, "_get_similar_formula", lambda x: "bar")
    # Act
    new_cmd = brew_install.get_new_command(dummy)
    # Assert
    assert new_cmd == "brew install bar"

def test_get_new_command_uses_first_error_in_output(monkeypatch):
    # Arrange
    dummy = DummyCommand(
        script="brew install baz",
        output=("Error: No available formula for qux\n"
                "Error: No available formula for baz\n")
    )
    # Patch helper to return a predictable replacement
    monkeypatch.setattr(brew_install, "_get_similar_formula", lambda x: "quux")
    # Act
    new_cmd = brew_install.get_new_command(dummy)
    # Assert that the first error term 'qux' was used for replacement
    assert new_cmd == "brew install quux"

def test_get_new_command_no_replacement_when_formula_same(monkeypatch):
    # Arrange
    dummy = DummyCommand(
        script="brew install alpha",
        output="Error: No available formula for alpha\n"
    )
    # Patch helper to return the same formula
    monkeypatch.setattr(brew_install, "_get_similar_formula", lambda x: "alpha")
    # Act
    new_cmd = brew_install.get_new_command(dummy)
    # Assert that the command remains unchanged
    assert new_cmd == "brew install alpha"
