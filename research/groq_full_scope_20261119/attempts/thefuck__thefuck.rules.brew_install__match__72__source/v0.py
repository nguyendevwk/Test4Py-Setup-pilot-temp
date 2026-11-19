import re
import types
import pytest
from thefuck.rules.brew_install import match, _get_similar_formula

# Helper command object
class Command:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_match_returns_true_for_similar_formula(monkeypatch):
    # Simulate get_closest returning a similar formula
    monkeypatch.setattr(
        "thefuck.rules.brew_install.get_closest",
        lambda formula, formulas: "similarformula"
    )
    cmd = Command(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "No available formula"
    )
    assert match(cmd) is True

def test_match_returns_false_when_no_similar_formula(monkeypatch):
    # Simulate get_closest returning None
    monkeypatch.setattr(
        "thefuck.rules.brew_install.get_closest",
        lambda formula, formulas: None
    )
    cmd = Command(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "No available formula"
    )
    assert match(cmd) is False

def test_match_returns_false_for_non_brew_command():
    cmd = Command(
        script="apt-get install nonexistent",
        output="Error: No available formula for nonexistent\n"
               "No available formula"
    )
    assert match(cmd) is False
