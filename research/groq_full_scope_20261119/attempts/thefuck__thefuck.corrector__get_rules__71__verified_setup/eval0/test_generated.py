import importlib
import sys
import types
import builtins
import pytest
from pathlib import Path

# Import the target module
from thefuck.corrector import get_rules
from thefuck import conf

@pytest.fixture(autouse=True)
def reset_settings(tmp_path):
    """Reset settings.rules_path to a clean state before each test."""
    conf.settings.rules_path = [tmp_path]
    yield
    # cleanup after test
    conf.settings.rules_path = []

def test_get_rules_ordering(tmp_path):
    """Test that get_rules returns rules sorted by priority."""
    # Create two rule files with different priorities
    rule_a = tmp_path / "rule_a.py"
    rule_a.write_text(
        """
from thefuck.types import Rule
class RuleA(Rule):
    priority = 10
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
"""
    )
    rule_b = tmp_path / "rule_b.py"
    rule_b.write_text(
        """
from thefuck.types import Rule
class RuleB(Rule):
    priority = 5
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
"""
    )

    # Reload the module to pick up the new settings
    importlib.reload(get_rules.__module__)

    rules = get_rules()
    # Assert that only two rules are loaded
    assert len(rules) == 2
    # Assert ordering by priority (ascending)
    assert [rule.priority for rule in rules] == [5, 10]
    # Assert that the rule classes are correctly named
    assert [rule.__class__.__name__ for rule in rules] == ["RuleB", "RuleA"]

def test_get_rules_empty(tmp_path):
    """Test that get_rules returns an empty list when no rule files exist."""
    # Ensure the directory is empty
    assert not any(tmp_path.iterdir())

    importlib.reload(get_rules.__module__)
    rules = get_rules()
    assert rules == []

def test_get_rules_skips_syntax_error(tmp_path):
    """Test that get_rules does not raise when encountering a syntax error."""
    # Valid rule
    valid_rule = tmp_path / "valid.py"
    valid_rule.write_text(
        """
from thefuck.types import Rule
class ValidRule(Rule):
    priority = 1
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
"""
    )
    # Invalid rule with syntax error
    invalid_rule = tmp_path / "invalid.py"
    invalid_rule.write_text(
        """
from thefuck.types import Rule
class InvalidRule(Rule):
    priority = 2
    def match(self, command):
        return False
    def get_new_command(self, command)
        return command
"""
    )

    importlib.reload(get_rules.__module__)
    rules = get_rules()
    # Only the valid rule should be loaded
    assert len(rules) == 1
    assert rules[0].__class__.__name__ == "ValidRule"
