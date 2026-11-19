import sys
import types
import importlib
import os
import pytest
from pathlib import Path

# Import the target Rule class from the package
from thefuck.types import Rule
from thefuck.conf import settings
from thefuck import logs

# Helper to create a dummy rule module file
def create_rule_file(tmp_path, name, content):
    file_path = tmp_path / f"{name}.py"
    file_path.write_text(content)
    return file_path

# Dummy Command class for testing
class DummyCommand:
    def __init__(self, output=None):
        self.output = output

# Test 1: Equality and representation of Rule instances
def test_rule_equality_and_repr():
    def dummy_match(cmd): return True
    def dummy_get_new(cmd): return "echo ok"
    def dummy_side(cmd, script): pass

    r1 = Rule("test", dummy_match, dummy_get_new, True, dummy_side, 10, False)
    r2 = Rule("test", dummy_match, dummy_get_new, True, dummy_side, 10, False)
    r3 = Rule("other", dummy_match, dummy_get_new, True, dummy_side, 10, False)

    # Equality
    assert r1 == r2
    assert r1 != r3

    # Representation contains all fields
    repr_str = repr(r1)
    assert "Rule(name=test" in repr_str
    assert "match=<function dummy_match" in repr_str
    assert "get_new_command=<function dummy_get_new" in repr_str
    assert "enabled_by_default=True" in repr_str
    assert "side_effect=<function dummy_side" in repr_str
    assert "priority=10" in repr_str
    assert "requires_output=False" in repr_str

# Test 2: from_path skips excluded rule and loads a valid rule
def test_rule_from_path_excluded_and_loaded(tmp_path):
    # Add a rule name to exclude
    settings.exclude_rules.add("excluded_rule")

    # Create excluded rule file
    excluded_path = create_rule_file(tmp_path, "excluded_rule", """
def match(cmd): return True
def get_new_command(cmd): return "echo excluded"
""")
    # Create a valid rule file
    valid_path = create_rule_file(tmp_path, "valid_rule", """
priority = 5
def match(cmd): return True
def get_new_command(cmd): return "echo valid"
""")

    # Load excluded rule
    excluded_rule = Rule.from_path(excluded_path)
    assert excluded_rule is None

    # Load valid rule
    loaded_rule = Rule.from_path(valid_path)
    assert isinstance(loaded_rule, Rule)
    assert loaded_rule.name == "valid_rule"
    assert loaded_rule.priority == 5
    # Ensure match and get_new_command are callable
    assert callable(loaded_rule.match)
    assert callable(loaded_rule.get_new_command)

# Test 3: is_match respects requires_output and handles exceptions
def test_rule_is_match_requires_output_and_exception_handling(tmp_path):
    # Rule that requires output
    def match_with_output(cmd):
        if cmd.output is None:
            raise ValueError("No output")
        return True

    rule = Rule(
        name="output_rule",
        match=match_with_output,
        get_new_command=lambda cmd: "echo ok",
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=True
    )

    # Command without output should not match
    cmd_no_output = DummyCommand(output=None)
    assert rule.is_match(cmd_no_output) is False

    # Command with output should match
    cmd_with_output = DummyCommand(output="some output")
    assert rule.is_match(cmd_with_output) is True

    # Rule that raises exception in match should not crash
    def match_raises(cmd): raise RuntimeError("fail")
    rule_raises = Rule(
        name="error_rule",
        match=match_raises,
        get_new_command=lambda cmd: "echo ok",
        enabled_by_default=True,
        side_effect=None,
        priority=1,
        requires_output=False
    )
    # Should return False and not propagate exception
    assert rule_raises.is_match(DummyCommand()) is False
