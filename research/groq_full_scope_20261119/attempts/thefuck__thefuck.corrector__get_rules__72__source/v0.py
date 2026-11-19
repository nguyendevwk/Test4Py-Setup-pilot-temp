import importlib
import sys
import types
import pathlib
import pytest

# Import the target function and related classes
from thefuck.corrector import get_rules
from thefuck.types import Rule


def _create_rule_file(tmp_path: pathlib.Path, name: str, priority: int = 10, body: str = "") -> pathlib.Path:
    """
    Helper to create a rule file that defines a Rule subclass.
    """
    rule_path = tmp_path / f"{name}.py"
    rule_path.write_text(
        f"""
from thefuck.types import Rule

class {name.capitalize()}Rule(Rule):
    priority = {priority}
    def match(self, command):
        return False
    def get_new_command(self, command):
        return command
{body}
"""
    )
    return rule_path


def _reload_module(module_name: str):
    """
    Reload a module and invalidate import caches.
    """
    if module_name in sys.modules:
        del sys.modules[module_name]
    importlib.invalidate_caches()
    return importlib.import_module(module_name)


def test_get_rules_normal(tmp_path: pathlib.Path):
    """
    Test that get_rules returns enabled rules from the temporary directory.
    """
    # Add tmp_path to sys.path so that the rules can be imported
    sys.path.insert(0, str(tmp_path))
    try:
        # Create two rule files with different priorities
        _create_rule_file(tmp_path, "alpha", priority=5)
        _create_rule_file(tmp_path, "beta", priority=1)

        # Reload the module to pick up new rules
        _reload_module("thefuck.corrector")

        rules = get_rules()
        # Ensure both rules are returned
        assert len(rules) == 2
        # Rules should be sorted by priority (ascending)
        assert [rule.priority for rule in rules] == [1, 5]
        # Ensure the rule classes are subclasses of Rule
        assert all(issubclass(type(rule), Rule) for rule in rules)
    finally:
        sys.path.pop(0)


def test_get_rules_empty(tmp_path: pathlib.Path):
    """
    Test that get_rules returns an empty list when no rule files are present.
    """
    sys.path.insert(0, str(tmp_path))
    try:
        # Ensure the directory is empty
        assert not any(tmp_path.iterdir())
        _reload_module("thefuck.corrector")
        rules = get_rules()
        assert rules == []
    finally:
        sys.path.pop(0)


def test_get_rules_error_handling(tmp_path: pathlib.Path):
    """
    Test that get_rules does not raise an exception when a rule file contains
    import-time errors. The faulty rule should be skipped.
    """
    sys.path.insert(0, str(tmp_path))
    try:
        # Create a valid rule
        _create_rule_file(tmp_path, "good", priority=2)

        # Create a faulty rule that raises during import
        faulty_path = tmp_path / "bad.py"
        faulty_path.write_text(
            """
raise RuntimeError("Import error in rule")
"""
        )

        _reload_module("thefuck.corrector")

        # get_rules should still return the good rule without propagating the error
        rules = get_rules()
        assert len(rules) == 1
        assert isinstance(rules[0], Rule)
        assert rules[0].priority == 2
    finally:
        sys.path.pop(0)
