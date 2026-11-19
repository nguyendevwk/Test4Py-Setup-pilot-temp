import importlib
import sys
import types
import os
import pytest

from thefuck.corrector import get_rules
from thefuck.conf import settings
from thefuck.types import Rule


def test_get_rules_order_and_priority(tmp_path):
    """Ensure get_rules returns rules sorted by priority."""
    # Create two rule modules with different priorities
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

    # Ensure the temporary directory is in the import paths
    sys.path.insert(0, str(tmp_path))
    # Point settings to our temporary rule directory
    settings.rule_dirs = [str(tmp_path)]

    # Import the modules so that get_loaded_rules can find them
    importlib.invalidate_caches()
    importlib.import_module("rule_a")
    importlib.import_module("rule_b")

    rules = get_rules()
    # The rules should be sorted by priority (5 then 10)
    assert [r.priority for r in rules] == [5, 10]
    # The rule classes should be RuleB and RuleA respectively
    assert [r.__class__.__name__ for r in rules] == ["RuleB", "RuleA"]


def test_get_rules_ignores_non_py(tmp_path):
    """Non‑Python files should not be considered as rules."""
    # Create a non‑Python file
    txt_file = tmp_path / "not_a_rule.txt"
    txt_file.write_text("Just some text")

    # Create a valid rule file
    rule = tmp_path / "valid_rule.py"
    rule.write_text(
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

    sys.path.insert(0, str(tmp_path))
    settings.rule_dirs = [str(tmp_path)]
    importlib.invalidate_caches()
    importlib.import_module("valid_rule")

    rules = get_rules()
    # Only the valid rule should be loaded
    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert rules[0].__class__.__name__ == "ValidRule"


def test_get_rules_syntax_error(tmp_path):
    """A rule file with a syntax error should raise ImportError."""
    bad_rule = tmp_path / "bad_rule.py"
    bad_rule.write_text(
        """
from thefuck.types import Rule
class BadRule(Rule):
    priority = 1
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
    def invalid_syntax
"""
    )

    sys.path.insert(0, str(tmp_path))
    settings.rule_dirs = [str(tmp_path)]
    importlib.invalidate_caches()

    with pytest.raises(ImportError):
        get_rules()
