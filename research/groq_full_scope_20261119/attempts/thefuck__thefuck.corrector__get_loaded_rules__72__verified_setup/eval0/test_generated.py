import importlib
import sys
import types
import pathlib

import pytest

from thefuck.corrector import get_loaded_rules
from thefuck.system import Path
from thefuck.types import Rule


def _create_rule_file(tmp_path, filename, enabled=True):
    """Create a simple rule file that defines a Rule subclass."""
    rule_code = f"""
from thefuck.types import Rule

class Rule(Rule):
    is_enabled = {enabled}
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
"""
    file_path = tmp_path / filename
    file_path.write_text(rule_code)
    return Path(file_path)


def test_rule_loaded(tmp_path):
    """A rule file with is_enabled=True should be yielded by get_loaded_rules."""
    rule_path = _create_rule_file(tmp_path, "rule1.py", enabled=True)
    rules = list(get_loaded_rules([rule_path]))
    assert len(rules) == 1
    rule = rules[0]
    assert isinstance(rule, Rule)
    assert rule.is_enabled is True
    # Ensure the rule instance can be used
    assert rule.match(None) is False
    assert rule.get_new_command(None) is None


def test_init_file_skipped(tmp_path):
    """A file named __init__.py should be ignored."""
    init_path = _create_rule_file(tmp_path, "__init__.py", enabled=True)
    rules = list(get_loaded_rules([init_path]))
    assert rules == []


def test_disabled_rule_not_yielded(tmp_path):
    """A rule file with is_enabled=False should not be yielded."""
    rule_path = _create_rule_file(tmp_path, "rule2.py", enabled=False)
    rules = list(get_loaded_rules([rule_path]))
    assert rules == []
