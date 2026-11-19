import os
import re
import types
import pytest
from thefuck.rules.brew_install import match, _get_similar_formula, _get_formulas

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_match_returns_true_for_similar_formula(tmp_path, monkeypatch):
    # Create a fake brew formula directory with a matching formula
    brew_dir = tmp_path / "Library" / "Formula"
    brew_dir.mkdir(parents=True)
    (brew_dir / "myformula.rb").write_text("# dummy formula")
    # Monkeypatch get_brew_path_prefix to point to our tmp_path
    monkeypatch.setattr(
        "thefuck.specific.brew.get_brew_path_prefix",
        lambda: str(tmp_path)
    )
    # Monkeypatch get_closest to return a non-empty string indicating a match
    monkeypatch.setattr(
        "thefuck.utils.get_closest",
        lambda name, formulas, cutoff: "myformula" if name == "myformula" else None
    )
    # Prepare command that triggers the match logic
    cmd = DummyCommand(
        script="brew install myformula",
        output="Error: No available formula for myformula\nNo available formula"
    )
    assert match(cmd) is True

def test_match_returns_false_when_no_similar_formula(tmp_path, monkeypatch):
    # Create a fake brew formula directory without the requested formula
    brew_dir = tmp_path / "Library" / "Formula"
    brew_dir.mkdir(parents=True)
    (brew_dir / "otherformula.rb").write_text("# dummy formula")
    # Monkeypatch get_brew_path_prefix to point to our tmp_path
    monkeypatch.setattr(
        "thefuck.specific.brew.get_brew_path_prefix",
        lambda: str(tmp_path)
    )
    # Monkeypatch get_closest to return None indicating no close match
    monkeypatch.setattr(
        "thefuck.utils.get_closest",
        lambda name, formulas, cutoff: None
    )
    cmd = DummyCommand(
        script="brew install nonexistent",
        output="Error: No available formula for nonexistent\nNo available formula"
    )
    assert match(cmd) is False

def test_match_returns_false_for_non_brew_command(tmp_path, monkeypatch):
    # Even if output contains the error string, script must be a brew install
    brew_dir = tmp_path / "Library" / "Formula"
    brew_dir.mkdir(parents=True)
    (brew_dir / "myformula.rb").write_text("# dummy formula")
    monkeypatch.setattr(
        "thefuck.specific.brew.get_brew_path_prefix",
        lambda: str(tmp_path)
    )
    monkeypatch.setattr(
        "thefuck.utils.get_closest",
        lambda name, formulas, cutoff: "myformula"
    )
    cmd = DummyCommand(
        script="apt-get install myformula",
        output="Error: No available formula for myformula\nNo available formula"
    )
    assert match(cmd) is False
