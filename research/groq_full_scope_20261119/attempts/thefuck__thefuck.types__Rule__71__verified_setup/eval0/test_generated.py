import types
import pytest
from thefuck.types import Rule

class DummyCommand:
    def __init__(self, output=None):
        self.output = output

def test_rule_equality_and_repr():
    """Rule equality compares all fields and repr shows them."""
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
    r3 = Rule(
        name="diff",
        match=lambda c: False,
        get_new_command=lambda c: "echo diff",
        enabled_by_default=False,
        side_effect=None,
        priority=5,
        requires_output=True,
    )
    assert r1 == r2
    assert r1 != r3
    assert "Rule(name=test" in repr(r1)

def test_is_match_requires_output():
    """When requires_output is True and command.output is None, is_match returns False."""
    rule = Rule(
        name="no_output",
        match=lambda c: True,
        get_new_command=lambda c: "echo",
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=True,
    )
    cmd_no_output = DummyCommand(output=None)
    cmd_with_output = DummyCommand(output="some output")
    # Should not match because output is None
    assert not rule.is_match(cmd_no_output)
    # Should match because output is present
    assert rule.is_match(cmd_with_output)

def test_get_corrected_commands_generates_expected():
    """get_corrected_commands yields CorrectedCommand objects with correct priority."""
    # Define a get_new_command that returns a list of two commands
    def get_new(cmd):
        return ["echo first", "echo second"]

    rule = Rule(
        name="multi",
        match=lambda c: True,
        get_new_command=get_new,
        enabled_by_default=True,
        side_effect=lambda cmd, script: None,
        priority=3,
        requires_output=False,
    )
    cmd = DummyCommand(output="irrelevant")
    corrected = list(rule.get_corrected_commands(cmd))
    # Two corrected commands should be produced
    assert len(corrected) == 2
    # Check that the scripts are as expected
    assert corrected[0].script == "echo first"
    assert corrected[1].script == "echo second"
    # Priority should be (index+1)*rule.priority
    assert corrected[0].priority == 3
    assert corrected[1].priority == 6
    # side_effect should be the same as rule.side_effect
    assert corrected[0].side_effect is rule.side_effect
    assert corrected[1].side_effect is rule.side_effect
