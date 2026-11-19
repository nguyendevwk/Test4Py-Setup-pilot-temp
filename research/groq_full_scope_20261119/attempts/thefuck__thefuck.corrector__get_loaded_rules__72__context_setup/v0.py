import importlib
import sys
import types
from pathlib import Path as PathLib

import pytest

from thefuck.corrector import get_loaded_rules
from thefuck.system import Path
from thefuck.types import Rule


def _create_rule_file(tmp_path, filename, class_name, enabled=True):
    """Create a rule file that defines a Rule subclass."""
    file_path = tmp_path / filename
    file_path.write_text(
        f"""
from thefuck.types import Rule

class {class_name}(Rule):
    is_enabled = {enabled}
"""
    )
    return Path(file_path)


def test_get_loaded_rules_yields_enabled_rule(tmp_path):
    """A rule file with is_enabled=True should be yielded."""
    rule_path = _create_rule_file(tmp_path, "my_rule.py", "MyRule")
    # Ensure the module can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        rules = list(get_loaded_rules([rule_path]))
        assert len(rules) == 1
        rule = rules[0]
        assert isinstance(rule, Rule)
        assert rule.__class__.__name__ == "MyRule"
        assert rule.is_enabled is True
    finally:
        sys.path.pop(0)


def test_get_loaded_rules_skips_init(tmp_path):
    """A file named __init__.py should be skipped."""
    init_path = _create_rule_file(tmp_path, "__init__.py", "InitRule")
    sys.path.insert(0, str(tmp_path))
    try:
        rules = list(get_loaded_rules([init_path]))
        assert rules == []
    finally:
        sys.path.pop(0)


def test_get_loaded_rules_skips_disabled_rule(tmp_path):
    """A rule file with is_enabled=False should not be yielded."""
    rule_path = _create_rule_file(tmp_path, "disabled_rule.py", "DisabledRule", enabled=False)
    sys.path.insert(0, str(tmp_path))
    try:
        rules = list(get_loaded_rules([rule_path]))
        assert rules == []
    finally:
        sys.path.pop(0)
