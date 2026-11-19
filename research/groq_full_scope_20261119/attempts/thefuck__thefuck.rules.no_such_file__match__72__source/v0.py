import re
import pytest
from thefuck.rules import no_such_file

class DummyCommand:
    def __init__(self, output):
        self.output = output

def test_match_returns_true_for_matching_output():
    # Pick a pattern from the module's patterns list that is known to match a typical error message.
    # We use the first pattern for simplicity.
    pattern = no_such_file.patterns[0]
    # Create an output that contains a substring matching the pattern.
    output = f"Error: No such file or directory: '{re.search(pattern, 'foo').group()}'"
    cmd = DummyCommand(output)
    assert no_such_file.match(cmd) is True

def test_match_returns_false_when_no_pattern_matches():
    # Use an output that does not match any pattern.
    output = "Some unrelated error message."
    cmd = DummyCommand(output)
    assert no_such_file.match(cmd) is False

def test_match_raises_attribute_error_when_output_missing():
    # Pass an object without an 'output' attribute to trigger AttributeError.
    class BadCommand:
        pass
    bad_cmd = BadCommand()
    with pytest.raises(AttributeError):
        no_such_file.match(bad_cmd)
