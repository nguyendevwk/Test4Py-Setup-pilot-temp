import re
import pytest
from thefuck.rules.brew_install import get_new_command
from thefuck.utils import replace_argument
from thefuck.specific.brew import get_brew_path_prefix, brew_available

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_formula(monkeypatch):
    # Arrange: mock get_closest to return a known formula
    monkeypatch.setattr(
        'thefuck.rules.brew_install.get_closest',
        lambda prefix, formula: f"{formula}_fixed"
    )
    # Mock replace_argument to perform a simple string replace
    monkeypatch.setattr(
        'thefuck.utils.replace_argument',
        lambda script, old, new: script.replace(old, new)
    )
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act
    new_cmd = get_new_command(cmd)
    # Assert
    assert new_cmd == "brew install foo_fixed"

def test_get_new_command_raises_when_no_match(monkeypatch):
    # Arrange: ensure get_closest is not called
    called = False
    def fake_get_closest(prefix, formula):
        nonlocal called
        called = True
        return "dummy"
    monkeypatch.setattr(
        'thefuck.rules.brew_install.get_closest',
        fake_get_closest
    )
    cmd = DummyCommand(
        script="brew install foo",
        output="Some unrelated error message"
    )
    # Act & Assert
    with pytest.raises(IndexError):
        get_new_command(cmd)
    assert not called, "get_closest should not be called when regex fails"

def test_get_new_command_uses_brew_path_prefix_and_brew_available(monkeypatch):
    # Arrange: patch get_brew_path_prefix and brew_available to verify they are called
    prefix_called = False
    brew_called = False
    def fake_prefix():
        nonlocal prefix_called
        prefix_called = True
        return "/usr/local"
    def fake_brew_available(formula):
        nonlocal brew_called
        brew_called = True
        return True
    monkeypatch.setattr(
        'thefuck.rules.brew_install.get_brew_path_prefix',
        fake_prefix
    )
    monkeypatch.setattr(
        'thefuck.rules.brew_install.brew_available',
        fake_brew_available
    )
    # Mock get_closest to return a formula that brew_available will accept
    monkeypatch.setattr(
        'thefuck.rules.brew_install.get_closest',
        lambda prefix, formula: "foo"
    )
    # Mock replace_argument to perform a simple string replace
    monkeypatch.setattr(
        'thefuck.utils.replace_argument',
        lambda script, old, new: script.replace(old, new)
    )
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act
    new_cmd = get_new_command(cmd)
    # Assert
    assert prefix_called, "get_brew_path_prefix should be called"
    assert brew_called, "brew_available should be called"
    assert new_cmd == "brew install foo"
