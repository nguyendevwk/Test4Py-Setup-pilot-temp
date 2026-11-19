import importlib
import sys
import types
import pathlib
import pytest

from thefuck.corrector import get_loaded_rules
from thefuck.types import Rule
from thefuck.system import Path


def create_rule_file(tmp_path, name, enabled=True, syntax_error=False):
    """Create a temporary rule file that defines a Rule subclass."""
    file_path = tmp_path / name
    if syntax_error:
        file_path.write_text("def bad syntax")
    else:
        content = f"""
from thefuck.types import Rule

class Rule(Rule):
    is_enabled = {enabled}
    def __init__(self, *args, **kwargs):
        pass
"""
        file_path.write_text(content)
    return Path(file_path)


def test_get_loaded_rules_yields_only_enabled(tmp_path):
    """Only enabled rules are yielded; disabled rules are skipped."""
    enabled_rule = create_rule_file(tmp_path, "enabled_rule.py", enabled=True)
    disabled_rule = create_rule_file(tmp_path, "disabled_rule.py", enabled=False)

    loaded = list(get_loaded_rules([enabled_rule, disabled_rule]))
    assert len(loaded) == 1
    assert isinstance(loaded[0], Rule)
    assert loaded[0].is_enabled is True


def test_get_loaded_rules_skips_init_file(tmp_path):
    """A file named __init__.py is never yielded, even if it defines an enabled rule."""
    init_rule = create_rule_file(tmp_path, "__init__.py", enabled=True)

    loaded = list(get_loaded_rules([init_rule]))
    assert loaded == []


def test_get_loaded_rules_handles_syntax_error(tmp_path):
    """Files with syntax errors are ignored without raising an exception."""
    bad_file = create_rule_file(tmp_path, "bad_rule.py", syntax_error=True)
    # The file is not an __init__.py, so Rule.from_path will try to import it.
    # It should not raise; the rule should simply not be yielded.
    loaded = list(get_loaded_rules([bad_file]))
    assert loaded == []
