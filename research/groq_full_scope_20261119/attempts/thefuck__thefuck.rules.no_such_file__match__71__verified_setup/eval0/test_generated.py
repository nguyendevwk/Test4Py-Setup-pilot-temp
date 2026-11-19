import re
import pytest
from thefuck.rules import no_such_file

# Helper command object mimicking the expected interface
class DummyCommand:
    def __init__(self, output):
        self.output = output

def test_match_returns_true_for_matching_output():
    """When the command output contains a known error pattern, match should return True."""
    # Pick a pattern from the module's patterns list (e.g., "No such file or directory")
    pattern = next((p for p in no_such_file.patterns if "No such file" in p), None)
    assert pattern is not None, "No suitable pattern found in the module."
    cmd = DummyCommand(output=f"cat: {pattern.split(':')[0]}: No such file or directory")
    assert no_such_file.match(cmd) is True

def test_match_returns_false_for_non_matching_output():
    """When the command output does not contain any known error pattern, match should return False."""
    cmd = DummyCommand(output="Some unrelated error message")
    assert no_such_file.match(cmd) is False

def test_match_raises_type_error_when_output_is_not_a_string():
    """The function should raise a TypeError if command.output is not a string."""
    cmd = DummyCommand(output=None)  # None is not a string
    with pytest.raises(TypeError):
        no_such_file.match(cmd)
