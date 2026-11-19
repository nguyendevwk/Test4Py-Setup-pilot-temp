import os
import re
import types
import pytest
from thefuck.rules import brew_install

# Helper to create a dummy command object
class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

@pytest.fixture
def brew_prefix(tmp_path):
    """Create a fake brew prefix with a single formula file."""
    brew_path = tmp_path / "brew"
    formula_dir = brew_path / "Library" / "Formula"
    formula_dir.mkdir(parents=True)
    # Create a formula file that matches the pattern used in _get_formulas
    (formula_dir / "example.rb").write_text("# example formula")
    return str(brew_path)

def test_match_returns_true_for_similar_formula(monkeypatch, brew_prefix):
    # Patch get_brew_path_prefix to return our fake prefix
    monkeypatch.setattr(brew_install, "get_brew_path_prefix", lambda: brew_prefix)
    # Patch get_closest to return a non-empty string indicating a match
    monkeypatch.setattr(brew_install, "get_closest", lambda name, formulas, cutoff: "example")
    # Command that should trigger the match logic
    cmd = DummyCommand(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\nNo available formula"
    )
    assert brew_install.match(cmd) is True

def test_match_returns_false_when_no_similar_formula(monkeypatch, brew_prefix):
    # Patch get_brew_path_prefix to return our fake prefix
    monkeypatch.setattr(brew_install, "get_brew_path_prefix", lambda: brew_prefix)
    # Patch get_closest to return None indicating no match
    monkeypatch.setattr(brew_install, "get_closest", lambda name, formulas, cutoff: None)
    cmd = DummyCommand(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\nNo available formula"
    )
    assert brew_install.match(cmd) is False

def test_match_returns_false_for_non_brew_command(monkeypatch, brew_prefix):
    # Even if output contains the error string, script must contain 'brew install'
    monkeypatch.setattr(brew_install, "get_brew_path_prefix", lambda: brew_prefix)
    cmd = DummyCommand(
        script="apt-get install nonexistent",
        output="Error: No available formula for nonexistent\nNo available formula"
    )
    assert brew_install.match(cmd) is False
