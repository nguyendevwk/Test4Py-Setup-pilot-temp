import importlib
import os
import sys
import types
import pytest

# Import the module under test
import thefuck.corrector as corrector


@pytest.fixture
def reload_corrector(monkeypatch):
    """Reload the corrector module after monkeypatching."""
    def _reload():
        importlib.reload(corrector)
    return _reload


def test_get_rules_empty(tmp_path, reload_corrector, monkeypatch):
    """
    When there are no rule files in any import path, get_rules should return an empty list.
    """
    # Ensure settings.user_dir points to an empty directory
    monkeypatch.setattr(corrector.settings, "user_dir", tmp_path)

    # Monkeypatch get_rules_import_paths to return only the empty tmp_path
    def fake_get_rules_import_paths():
        yield tmp_path
    monkeypatch.setattr(corrector, "get_rules_import_paths", fake_get_rules_import_paths)

    reload_corrector()
    assert corrector.get_rules() == []


def test_get_rules_sorting(tmp_path, reload_corrector, monkeypatch):
    """
    Rules should be sorted by their priority attribute.
    """
    # Create two rule files in a temporary directory
    rule_a_path = tmp_path / "rule_a.py"
    rule_b_path = tmp_path / "rule_b.py"

    rule_a_path.write_text(
        """
from thefuck.types import Rule

class RuleA(Rule):
    priority = 10
    def is_enabled(self):
        return True
"""
    )
    rule_b_path.write_text(
        """
from thefuck.types import Rule

class RuleB(Rule):
    priority = 5
    def is_enabled(self):
        return True
"""
    )

    # Monkeypatch get_rules_import_paths to yield our temp directory
    def fake_get_rules_import_paths():
        yield tmp_path
    monkeypatch.setattr(corrector, "get_rules_import_paths", fake_get_rules_import_paths)

    reload_corrector()
    rules = corrector.get_rules()
    # The rules should be sorted by priority: RuleB (5) before RuleA (10)
    assert [rule.__class__.__name__ for rule in rules] == ["RuleB", "RuleA"]


def test_get_rules_user_dir(tmp_path, reload_corrector, monkeypatch):
    """
    Rules defined in the user's directory should be included in the result.
    """
    # Create a rule file in the user directory
    user_rule_path = tmp_path / "user_rule.py"
    user_rule_path.write_text(
        """
from thefuck.types import Rule

class UserRule(Rule):
    priority = 1
    def is_enabled(self):
        return True
"""
    )

    # Point settings.user_dir to the temporary directory
    monkeypatch.setattr(corrector.settings, "user_dir", tmp_path)

    # Monkeypatch get_rules_import_paths to yield only the user directory
    def fake_get_rules_import_paths():
        yield tmp_path
    monkeypatch.setattr(corrector, "get_rules_import_paths", fake_get_rules_import_paths)

    reload_corrector()
    rules = corrector.get_rules()
    assert len(rules) == 1
    assert rules[0].__class__.__name__ == "UserRule"
