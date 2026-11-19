import re
import types
import pytest
from thefuck.rules.brew_install import match, _get_similar_formula

# Helper to create a minimal command object
class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_match_returns_true_for_similar_formula(monkeypatch):
    # Simulate that get_closest finds a similar formula
    def fake_get_closest(formula, candidates):
        return "similar_formula"
    monkeypatch.setattr("thefuck.utils.get_closest", fake_get_closest)

    cmd = DummyCommand(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "  Did you mean: similar_formula?"
    )
    assert match(cmd) is True

def test_match_returns_false_when_no_similar_formula(monkeypatch):
    # Simulate that get_closest returns None (no similar formula)
    def fake_get_closest(formula, candidates):
        return None
    monkeypatch.setattr("thefuck.utils.get_closest", fake_get_closest)

    cmd = DummyCommand(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "  Did you mean: similar_formula?"
    )
    assert match(cmd) is False

def test_match_returns_false_for_non_brew_command():
    cmd = DummyCommand(
        script="apt-get install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "  Did you mean: similar_formula?"
    )
    assert match(cmd) is False
