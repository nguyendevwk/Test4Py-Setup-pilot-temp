import importlib
import sys
import types
import builtins
import pytest

# Import the target function and related objects
from thefuck.corrector import get_rules
from thefuck.conf import settings
from thefuck.types import Rule
from thefuck.system import Path


def _create_rule_file(tmp_path, name, priority=None, raise_error=False):
    """Create a temporary rule file that defines a Rule subclass."""
    content = []
    if raise_error:
        content.append("raise RuntimeError('import error')")
    else:
        content.append("from thefuck.types import Rule")
        content.append(f"class {name}(Rule):")
        if priority is not None:
            content.append(f"    priority = {priority}")
        else:
            content.append("    pass")
    file_path = tmp_path / f"{name}.py"
    file_path.write_text("\n".join(content))
    return file_path


def test_get_rules_order_and_priority(tmp_path):
    """Test that get_rules returns enabled rules sorted by priority."""
    # Monkey‑patch the settings to point to our temporary directory
    settings.rules_path = [Path(tmp_path)]

    # Create two rule files with different priorities
    _create_rule_file(tmp_path, "RuleA", priority=10)
    _create_rule_file(tmp_path, "RuleB", priority=5)

    # Reload the module to ensure it sees the new settings
    importlib.reload(sys.modules["thefuck.corrector"])

    rules = get_rules()

    # Verify that we got two Rule instances
    assert len(rules) == 2
    assert all(isinstance(r, Rule) for r in rules)

    # Verify that the rules are sorted by priority (ascending)
    priorities = [r.priority for r in rules]
    assert priorities == sorted(priorities)


def test_get_rules_empty_directory(tmp_path):
    """Test that get_rules returns an empty list when no rule files are present."""
    settings.rules_path = [Path(tmp_path)]
    importlib.reload(sys.modules["thefuck.corrector"])
    rules = get_rules()
    assert rules == []


def test_get_rules_handles_import_errors(tmp_path):
    """Test that get_rules does not raise when a rule file raises an exception on import."""
    settings.rules_path = [Path(tmp_path)]
    # Create a rule file that raises an exception during import
    _create_rule_file(tmp_path, "BadRule", raise_error=True)
    # Also create a valid rule to ensure that valid rules are still loaded
    _create_rule_file(tmp_path, "GoodRule", priority=1)

    importlib.reload(sys.modules["thefuck.corrector"])
    # get_rules should return the good rule without propagating the import error
    rules = get_rules()
    assert len(rules) == 1
    assert isinstance(rules[0], Rule)
    assert rules[0].__class__.__name__ == "GoodRule"
