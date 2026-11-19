import pathlib
import pytest
from thefuck.corrector import get_loaded_rules
from thefuck.types import Rule

def test_get_loaded_rules_empty_list():
    """When no paths are provided, the generator yields nothing."""
    rules = list(get_loaded_rules([]))
    assert rules == []

def test_get_loaded_rules_skips_init(tmp_path):
    """Files named '__init__.py' are skipped regardless of rule status."""
    # Create a dummy __init__.py file
    init_file = tmp_path / "__init__.py"
    init_file.write_text("# dummy init")
    # The generator should skip this file
    rules = list(get_loaded_rules([init_file]))
    assert rules == []

def test_get_loaded_rules_yields_enabled_rule(tmp_path):
    """A rule file that defines an enabled Rule is yielded."""
    # Create a simple rule file that defines a Rule subclass
    rule_file = tmp_path / "dummy_rule.py"
    rule_file.write_text(
        """
from thefuck.types import Rule

class DummyRule(Rule):
    def __init__(self):
        super().__init__()
        self.is_enabled = True
"""
    )
    # Import the module to ensure it is discoverable
    import importlib.util
    spec = importlib.util.spec_from_file_location("dummy_rule", rule_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Now get the rule via get_loaded_rules
    rules = list(get_loaded_rules([rule_file]))
    assert len(rules) == 1
    rule = rules[0]
    assert isinstance(rule, Rule)
    assert rule.is_enabled is True
