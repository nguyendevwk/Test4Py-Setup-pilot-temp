import re
import os
import pytest
from thefuck.rules.brew_install import get_new_command, _get_similar_formula, _get_formulas
from types import SimpleNamespace

# Helper to create a dummy command object
def make_command(script, output):
    return SimpleNamespace(script=script, output=output)

# Test normal behavior: a missing formula is suggested correctly
def test_get_new_command_replaces_with_similar(monkeypatch, tmp_path):
    # Prepare a fake formula list
    fake_formula = "foo"
    similar_formula = "foobar"
    # Monkeypatch get_closest to return the similar formula
    monkeypatch.setattr("thefuck.utils.get_closest", lambda name, formulas, cutoff: similar_formula)
    # Monkeypatch replace_argument to simply return the new script
    monkeypatch.setattr("thefuck.utils.replace_argument", lambda script, old, new: script.replace(old, new))
    # Create a command that triggers the rule
    cmd = make_command("brew install foo", "Error: No available formula for foo")
    new_cmd = get_new_command(cmd)
    assert new_cmd == "brew install foobar"

# Test boundary: when no formulas are available, _get_formulas yields nothing
def test_get_similar_formula_no_formulas(monkeypatch):
    # Monkeypatch get_brew_path_prefix to raise to trigger exception in _get_formulas
    monkeypatch.setattr("thefuck.specific.brew.get_brew_path_prefix", lambda: "/nonexistent")
    # Ensure _get_formulas yields nothing
    assert list(_get_formulas()) == []
    # get_closest should be called with empty list; monkeypatch to return None
    monkeypatch.setattr("thefuck.utils.get_closest", lambda name, formulas, cutoff: None)
    result = _get_similar_formula("foo")
    assert result is None

# Test error behavior: command output does not match regex
def test_get_new_command_no_match_raises(monkeypatch):
    cmd = make_command("brew install foo", "Some unrelated output")
    with pytest.raises(IndexError):
        get_new_command(cmd)
