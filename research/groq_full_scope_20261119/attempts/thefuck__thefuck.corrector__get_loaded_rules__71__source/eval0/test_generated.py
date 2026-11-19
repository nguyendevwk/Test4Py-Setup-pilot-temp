import importlib
import sys
import types
import pathlib
import pytest

# Import the target function and supporting classes
from thefuck.corrector import get_loaded_rules
from thefuck.types import Rule
from thefuck.system import Path

def write_rule_file(tmp_path, name, enabled=True):
    """Create a minimal rule file that defines a Rule subclass."""
    content = f"""
from thefuck.types import Rule

class {name}(Rule):
    is_enabled = {enabled}

    def match(self, command):
        return False

    def correct(self, command):
        return command
"""
    file_path = tmp_path / f"{name}.py"
    file_path.write_text(content)
    return Path(file_path)

def test_get_loaded_rules_skips_init(tmp_path):
    """Ensure that a file named '__init__.py' is not yielded."""
    init_file = tmp_path / "__init__.py"
    init_file.write_text("")  # empty init file
    paths = [Path(init_file)]
    rules = list(get_loaded_rules(paths))
    assert rules == [], "Expected no rules to be loaded from __init__.py"

def test_get_loaded_rules_yields_enabled_rule(tmp_path):
    """A rule with is_enabled=True should be yielded."""
    rule_path = write_rule_file(tmp_path, "EnabledRule", enabled=True)
    rules = list(get_loaded_rules([rule_path]))
    assert len(rules) == 1, "Expected one rule to be loaded"
    rule = rules[0]
    assert isinstance(rule, Rule), "Loaded object should be an instance of Rule"
    assert rule.is_enabled is True, "Rule should be enabled"

def test_get_loaded_rules_skips_disabled_rule(tmp_path):
    """A rule with is_enabled=False should not be yielded."""
    rule_path = write_rule_file(tmp_path, "DisabledRule", enabled=False)
    rules = list(get_loaded_rules([rule_path]))
    assert rules == [], "Expected no rules to be loaded when is_enabled is False"
