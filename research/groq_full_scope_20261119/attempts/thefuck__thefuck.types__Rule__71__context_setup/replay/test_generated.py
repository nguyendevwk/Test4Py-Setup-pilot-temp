import pytest
from pathlib import Path
from thefuck.types import Rule, CorrectedCommand
from thefuck.conf import settings

# Dummy command class for testing
class DummyCommand:
    def __init__(self, output=None):
        self.output = output

def test_rule_equality_and_repr():
    """Rule equality should compare all fields and repr should be informative."""
    r1 = Rule(
        name="test",
        match=lambda c: True,
        get_new_command=lambda c: "echo ok",
        enabled_by_default=True,
        side_effect=None,
        priority=10,
        requires_output=False,
    )
    r2 = Rule(
        name="test",
        match=r1.match,
        get_new_command=r1.get_new_command,
        enabled_by_default=True,
        side_effect=None,
        priority=10,
        requires_output=False,
    )
    assert r1 == r2
    assert repr(r1).startswith("Rule(name=test")

def test_is_match_requires_output():
    """Rule should not match when requires_output is True and command has no output."""
    r = Rule(
        name="no_output",
        match=lambda c: True,
        get_new_command=lambda c: "echo ok",
        enabled_by_default=True,
        side_effect=None,
        priority=5,
        requires_output=True,
    )
    cmd_no_output = DummyCommand(output=None)
    cmd_with_output = DummyCommand(output="some output")
    # Should be False because requires_output and no output
    assert not r.is_match(cmd_no_output)
    # Should be True when output is present
    assert r.is_match(cmd_with_output)

def test_get_corrected_commands_multiple_and_priority():
    """get_corrected_commands should yield CorrectedCommand objects with correct priority."""
    def get_new(cmd):
        return ["cmd1", "cmd2"]
    r = Rule(
        name="multi",
        match=lambda c: True,
        get_new_command=get_new,
        enabled_by_default=True,
        side_effect=lambda c, s: None,
        priority=3,
        requires_output=False,
    )
    cmd = DummyCommand(output="out")
    corrected = list(r.get_corrected_commands(cmd))
    assert len(corrected) == 2
    # First command priority should be 1*3=3, second 2*3=6
    assert corrected[0].priority == 3
    assert corrected[1].priority == 6
    # Scripts should match the returned list
    assert corrected[0].script == "cmd1"
    assert corrected[1].script == "cmd2"
