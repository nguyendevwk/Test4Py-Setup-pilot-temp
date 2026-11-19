import re
import types
import pytest
from thefuck.rules.brew_install import match, _get_similar_formula

# Helper to create a minimal command object
class DummyCommand:
    def __init__(self, script: str, output: str):
        self.script = script
        self.output = output

def test_match_returns_true_for_similar_formula():
    """
    When the command is a brew install that fails with a missing formula,
    and a similar formula exists, match should return True.
    """
    # Simulate a missing formula for 'foo' and a similar available formula 'foobar'
    script = "brew install foo"
    output = "Error: No available formula for foo\n" \
             "No available formula\n" \
             "Error: No available formula for foobar"
    # Ensure that _get_similar_formula finds a similar formula
    assert _get_similar_formula("foo") is not None
    cmd = DummyCommand(script, output)
    assert match(cmd) is True

def test_match_returns_false_when_no_similar_formula():
    """
    When the command is a brew install that fails with a missing formula,
    but no similar formula exists, match should return False.
    """
    script = "brew install nonexistent"
    output = "Error: No available formula for nonexistent\n" \
             "No available formula\n"
    # Ensure that _get_similar_formula returns None for a truly unknown formula
    assert _get_similar_formula("nonexistent") is None
    cmd = DummyCommand(script, output)
    assert match(cmd) is False

def test_match_returns_false_for_non_brew_command():
    """
    When the command is not a brew install or the output does not contain
    the expected error message, match should return False.
    """
    script = "apt-get install foo"
    output = "E: Unable to locate package foo"
    cmd = DummyCommand(script, output)
    assert match(cmd) is False
