import pytest
from pathlib import Path as PyPath
from thefuck.corrector import get_loaded_rules
from thefuck.system import Path as ThefuckPath
from thefuck.types import Rule

def test_get_loaded_rules_skips_init(tmp_path):
    """`get_loaded_rules` should skip files named '__init__.py'."""
    # Create a dummy rule file that would normally be loaded
    rule_file = tmp_path / "dummy_rule.py"
    rule_file.write_text(
        """
from thefuck.types import Rule

class DummyRule(Rule):
    is_enabled = True
"""
    )
    # Create an __init__.py file that should be ignored
    init_file = tmp_path / "__init__.py"
    init_file.write_text("# init")

    # Convert to ThefuckPath objects
    paths = [ThefuckPath(p) for p in [rule_file, init_file]]
    loaded = list(get_loaded_rules(paths))

    # Only the dummy rule should be loaded
    assert len(loaded) == 1
    assert isinstance(loaded[0], Rule)
    assert loaded[0].is_enabled is True

def test_get_loaded_rules_empty_list():
    """When no paths are provided, the generator yields nothing."""
    assert list(get_loaded_rules([])) == []

def test_get_loaded_rules_invalid_path_raises():
    """Passing an object without a 'name' attribute should raise AttributeError."""
    class Dummy:
        pass

    with pytest.raises(AttributeError):
        list(get_loaded_rules([Dummy()]))
