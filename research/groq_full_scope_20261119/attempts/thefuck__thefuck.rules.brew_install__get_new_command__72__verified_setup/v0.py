import re
import pytest
from thefuck.rules.brew_install import get_new_command
from thefuck.utils import replace_argument

# A minimal Command stub used by the rule
class Command:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def test_get_new_command_replaces_missing_formula(monkeypatch):
    # Simulate a brew error message for a missing formula
    cmd = Command(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Monkeypatch get_closest to return a known similar formula
    monkeypatch.setattr(
        "thefuck.rules.brew_install.get_closest",
        lambda x, y: "bar"
    )
    new_cmd = get_new_command(cmd)
    # The new command should replace 'foo' with 'bar'
    assert new_cmd == "brew install bar"

def test_get_new_command_handles_multiple_occurrences(monkeypatch):
    # Simulate a command with the missing formula appearing twice
    cmd = Command(
        script="brew install foo && brew install foo",
        output="Error: No available formula for foo\n"
    )
    # get_closest returns 'baz'
    monkeypatch.setattr(
        "thefuck.rules.brew_install.get_closest",
        lambda x, y: "baz"
    )
    new_cmd = get_new_command(cmd)
    # All occurrences of 'foo' should be replaced with 'baz'
    assert new_cmd == "brew install baz && brew install baz"

def test_get_new_command_raises_when_no_formula_found(monkeypatch):
    # Simulate output that does not contain the expected pattern
    cmd = Command(
        script="brew install foo",
        output="Some unrelated error message\n"
    )
    # get_closest should not be called because the regex will fail
    called = False
    def fake_get_closest(*args, **kwargs):
        nonlocal called
        called = True
        return "dummy"
    monkeypatch.setattr(
        "thefuck.rules.brew_install.get_closest",
        fake_get_closest
    )
    with pytest.raises(IndexError):
        get_new_command(cmd)
    # Ensure get_closest was never called
    assert not called
