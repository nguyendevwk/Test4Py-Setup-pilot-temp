import pytest
from thefuck.corrector import get_corrected_commands
from thefuck.types import Command, CorrectedCommand

def test_corrected_command_exists(tmp_path):
    # A command that is known to match a rule (e.g., a misspelled git command)
    cmd = Command("git commt", None)
    corrected = list(get_corrected_commands(cmd))
    # There should be at least one corrected command
    assert corrected, "Expected at least one corrected command"
    # The first corrected command should be a CorrectedCommand instance
    assert isinstance(corrected[0], CorrectedCommand)
    # The corrected command string should be the expected one
    assert corrected[0].command == "git commit"

def test_corrected_commands_unique_and_sorted(tmp_path):
    # Use a command that triggers multiple corrections (e.g., a pip command with typo)
    cmd = Command("pip installe", None)
    corrected = list(get_corrected_commands(cmd))
    # Ensure there are multiple corrections
    assert len(corrected) > 1, "Expected multiple corrections for pip typo"
    # Extract the command strings
    commands = [c.command for c in corrected]
    # Commands should be sorted alphabetically
    assert commands == sorted(commands), "Commands are not sorted"
    # Commands should be unique
    assert len(commands) == len(set(commands)), "Duplicate corrected commands found"

def test_no_match_returns_empty(tmp_path):
    # A command that does not match any rule
    cmd = Command("thiscommanddoesnotexist", None)
    corrected = list(get_corrected_commands(cmd))
    # The generator should yield nothing
    assert corrected == [], "Expected no corrected commands for unmatched input"
