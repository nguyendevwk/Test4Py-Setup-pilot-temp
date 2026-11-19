import re
import pytest
from thefuck.rules import no_such_file

# Helper to create a simple command-like object
class DummyCommand:
    def __init__(self, output):
        self.output = output

def test_match_returns_true_for_each_pattern():
    """The match function should return True when the command output contains any of the patterns."""
    # Use the actual patterns defined in the module
    for pattern in no_such_file.patterns:
        # Construct an output that definitely matches the pattern
        # We use a simple string that contains the pattern literally
        output = f"Error: {pattern}"
        cmd = DummyCommand(output)
        assert no_such_file.match(cmd) is True, f"Pattern {pattern!r} should match"

def test_match_returns_false_for_non_matching_output():
    """The match function should return False when the command output does not match any pattern."""
    # Pick a string that is unlikely to match any pattern
    output = "This is a harmless message with no errors."
    cmd = DummyCommand(output)
    assert no_such_file.match(cmd) is False

def test_match_handles_empty_output_without_error():
    """The match function should handle an empty output string gracefully and return False."""
    cmd = DummyCommand("")
    assert no_such_file.match(cmd) is False
