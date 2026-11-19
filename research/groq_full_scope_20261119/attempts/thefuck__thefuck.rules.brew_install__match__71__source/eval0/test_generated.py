import re
import types
import pytest
from thefuck.rules.brew_install import match

# Helper to create a simple command object with script and output attributes
class DummyCommand:
    def __init__(self, script: str, output: str):
        self.script = script
        self.output = output

def test_match_returns_true_for_similar_formula(tmp_path):
    """
    When the command is a brew install that fails with a missing formula,
    and a similar formula exists, match should return True.
    """
    # Use a known formula that likely has a close match in Homebrew
    script = "brew install nonexistentformula"
    output = (
        "Error: No available formula for nonexistentformula\n"
        "Did you mean: 'nonexistentformul'?"
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is True

def test_match_returns_false_when_no_similar_formula(tmp_path):
    """
    If no similar formula can be found, match should return False.
    """
    script = "brew install abcxyz"
    output = (
        "Error: No available formula for abcxyz\n"
        "No suggestions available."
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is False

def test_match_returns_false_for_non_brew_command(tmp_path):
    """
    If the command is not a brew install, match should return False regardless of output.
    """
    script = "apt-get install nonexistent"
    output = (
        "Error: No available formula for nonexistent\n"
        "Did you mean: 'nonexistent'?"
    )
    cmd = DummyCommand(script, output)
    assert match(cmd) is False
