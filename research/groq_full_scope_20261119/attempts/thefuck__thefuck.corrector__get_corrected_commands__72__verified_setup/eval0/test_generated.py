import pytest
from thefuck.corrector import get_corrected_commands
from thefuck.types import Command, CorrectedCommand

def test_get_corrected_commands_normal():
    # A command that matches a known rule (git commit typo)
    cmd = Command("git commt", None, None, None, None, None, None, None, None)
    corrected = list(get_corrected_commands(cmd))
    # Expect at least one corrected command
    assert any(isinstance(c, CorrectedCommand) for c in corrected)
    # The most common correction should be "git commit"
    assert any(c.command == "git commit" for c in corrected)

def test_get_corrected_commands_no_match():
    # A nonsense command that should not match any rule
    cmd = Command("asdfghjkl", None, None, None, None, None, None, None, None)
    corrected = list(get_corrected_commands(cmd))
    # No corrections should be returned
    assert corrected == []

def test_get_corrected_commands_sorted_and_unique(tmp_path):
    # Use a command that triggers multiple rules producing the same correction
    # For example, "python3 -m pip install" can be corrected to both
    # "pip install" and "pip3 install" by different rules.
    cmd = Command("python3 -m pip install", None, None, None, None, None, None, None, None)
    corrected = list(get_corrected_commands(cmd))
    # Extract command strings
    commands = [c.command for c in corrected]
    # Ensure no duplicates
    assert len(commands) == len(set(commands))
    # Ensure commands are sorted alphabetically
    assert commands == sorted(commands)
