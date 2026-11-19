import builtins
import importlib
import os
import sys
import types
import pytest
from pathlib import Path

# Import the Rule class from the real module
from thefuck.types import Rule
from thefuck import settings, logs

# Helper to create a temporary rule file
def create_rule_file(tmp_path, name, content):
    path = tmp_path / f"{name}.py"
    path.write_text(content)
    return path

def test_rule_from_path_excluded(tmp_path):
    """Rule.from_path should return None for an excluded rule."""
    # Add a rule name to the excluded list
    settings.exclude_rules.add("excluded_rule")
    rule_path = create_rule_file(tmp_path, "excluded_rule", """
def match(cmd): return True
def get_new_command(cmd): return "echo ok"
""")
    # Ensure the rule is excluded
    rule = Rule.from_path(rule_path)
    assert rule is None
    # Clean up
    settings.exclude_rules.remove("excluded_rule")

def test_rule_is_match_requires_output_false(tmp_path):
    """Rule.is_match should return True when requires_output is False and command has no output."""
    # Create a simple rule that matches any command
    rule_path = create_rule_file(tmp_path, "always_match", """
def match(cmd): return True
def get_new_command(cmd): return "echo matched"
requires_output = False
""")
    rule = Rule.from_path(rule_path)
    assert rule is not None
    # Create a dummy command object with output=None
    Command = types.SimpleNamespace
    cmd = Command(output=None)
    assert rule.is_match(cmd) is True

def test_rule_get_corrected_commands_and_repr(tmp_path):
    """get_corrected_commands should yield CorrectedCommand objects with correct priority and __repr__ should be informative."""
    # Create a rule that returns two new commands
    rule_path = create_rule_file(tmp_path, "two_commands", """
def match(cmd): return True
def get_new_command(cmd): return ["echo first", "echo second"]
priority = 10
""")
    rule = Rule.from_path(rule_path)
    assert rule is not None
    # Dummy command
    Command = types.SimpleNamespace
    cmd = Command(output="some output")
    corrected = list(rule.get_corrected_commands(cmd))
    # Two corrected commands
    assert len(corrected) == 2
    # Check priorities: first should be 10, second 20
    assert corrected[0].priority == 10
    assert corrected[1].priority == 20
    # __repr__ should include the rule name and other attributes
    repr_str = repr(rule)
    assert "two_commands" in repr_str
    assert "match" in repr_str
    assert "get_new_command" in repr_str
    assert "priority=10" in repr_str
