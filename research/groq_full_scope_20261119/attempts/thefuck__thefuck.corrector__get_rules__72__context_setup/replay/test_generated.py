import sys
import types
import importlib
import pathlib
import pytest

# Import the target function and related helpers
from thefuck.corrector import get_rules, get_rules_import_paths, get_loaded_rules
from thefuck.types import Rule
from thefuck.conf import settings

# Helper to create a dummy rule file
def create_rule_file(path: pathlib.Path, name: str):
    (path / f"{name}.py").write_text(f"# dummy rule {name}\n")

# Test 1: Normal behavior – one enabled rule in bundled path
def test_get_rules_single_enabled_rule(tmp_path, monkeypatch):
    # Prepare a fake bundled rules directory
    bundled = tmp_path / "bundled_rules"
    bundled.mkdir()
    create_rule_file(bundled, "rule_a")

    # Monkeypatch the import path to point to our fake bundled directory
    monkeypatch.setattr(
        "thefuck.corrector.get_rules_import_paths",
        lambda: [bundled]
    )

    # Mock Rule.from_path to return a simple object with priority and is_enabled
    class DummyRule:
        def __init__(self, name, priority):
            self.name = name
            self.priority = priority
            self.is_enabled = True

    def fake_from_path(path):
        return DummyRule(path.stem, priority=10)

    monkeypatch.setattr(Rule, "from_path", staticmethod(fake_from_path))

    # Call the function under test
    rules = get_rules()

    # Assertions
    assert len(rules) == 1
    assert rules[0].name == "rule_a"
    assert rules[0].priority == 10

# Test 2: Boundary behavior – __init__.py should be ignored
def test_get_rules_ignore_init(tmp_path, monkeypatch):
    # Create a bundled rules directory with an __init__.py and a real rule
    bundled = tmp_path / "bundled_rules"
    bundled.mkdir()
    (bundled / "__init__.py").write_text("")
    create_rule_file(bundled, "rule_b")

    monkeypatch.setattr(
        "thefuck.corrector.get_rules_import_paths",
        lambda: [bundled]
    )

    class DummyRule:
        def __init__(self, name, priority):
            self.name = name
            self.priority = priority
            self.is_enabled = True

    def fake_from_path(path):
        return DummyRule(path.stem, priority=5)

    monkeypatch.setattr(Rule, "from_path", staticmethod(fake_from_path))

    rules = get_rules()

    # Assertions
    assert len(rules) == 1
    assert rules[0].name == "rule_b"
    assert rules[0].priority == 5

# Test 3: Error handling – Rule.from_path returns None for a rule
def test_get_rules_skip_disabled(tmp_path, monkeypatch):
    # Prepare bundled rules with two files
    bundled = tmp_path / "bundled_rules"
    bundled.mkdir()
    create_rule_file(bundled, "rule_c")
    create_rule_file(bundled, "rule_d")

    monkeypatch.setattr(
        "thefuck.corrector.get_rules_import_paths",
        lambda: [bundled]
    )

    class DummyRule:
        def __init__(self, name, priority, enabled):
            self.name = name
            self.priority = priority
            self.is_enabled = enabled

    def fake_from_path(path):
        if path.stem == "rule_c":
            return DummyRule("rule_c", priority=2, enabled=True)
        else:
            # Simulate a rule that is disabled or invalid
            return DummyRule("rule_d", priority=1, enabled=False)

    monkeypatch.setattr(Rule, "from_path", staticmethod(fake_from_path))

    rules = get_rules()

    # Assertions
    assert len(rules) == 1
    assert rules[0].name == "rule_c"
    assert rules[0].priority == 2
