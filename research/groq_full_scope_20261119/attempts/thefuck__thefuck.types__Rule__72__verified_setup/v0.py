import types
import pytest
from thefuck.types import Rule

class DummyCommand:
    def __init__(self, output=None):
        self.output = output

def test_is_match_requires_output_false():
    # Rule requires output but command has no output
    rule = Rule(
        name="test",
        match=lambda cmd: True,
        get_new_command=lambda cmd: "echo ok",
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=True,
    )
    cmd = DummyCommand(output=None)
    assert rule.is_match(cmd) is False

def test_get_corrected_commands_priority_and_side_effect():
    # get_new_command returns a list of two commands
    def get_new(cmd):
        return ["cmd1", "cmd2"]
    rule = Rule(
        name="multi",
        match=lambda cmd: True,
        get_new_command=get_new,
        enabled_by_default=True,
        side_effect=lambda cmd, script: None,
        priority=2,
        requires_output=False,
    )
    cmd = DummyCommand(output="anything")
    corrected = list(rule.get_corrected_commands(cmd))
    # Two corrected commands
    assert len(corrected) == 2
    # First has priority 2, second 4
    assert corrected[0].priority == 2
    assert corrected[1].priority == 4
    # Scripts match
    assert corrected[0].script == "cmd1"
    assert corrected[1].script == "cmd2"
    # Side effect is the same function
    assert corrected[0].side_effect is rule.side_effect

def test_rule_equality_and_repr():
    rule1 = Rule(
        name="eq",
        match=lambda cmd: True,
        get_new_command=lambda cmd: "ok",
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=False,
    )
    # Create an identical rule
    rule2 = Rule(
        name="eq",
        match=rule1.match,
        get_new_command=rule1.get_new_command,
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=False,
    )
    # Different match function
    rule3 = Rule(
        name="eq",
        match=lambda cmd: False,
        get_new_command=rule1.get_new_command,
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=False,
    )
    assert rule1 == rule2
    assert rule1 != rule3
    # Representation contains all fields
    rep = repr(rule1)
    assert "Rule(name=eq" in rep
    assert "match=" in rep
    assert "get_new_command=" in rep
    assert "enabled_by_default=True" in rep
    assert "side_effect=None" in rep
    assert "priority=1" in rep
    assert "requires_output=False" in rep
