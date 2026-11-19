import pytest
from collections import namedtuple

# Import the target function
from thefuck.corrector import organize_commands

# Define a minimal CorrectedCommand type for testing
CorrectedCommand = namedtuple('CorrectedCommand', ['command', 'priority'])

def test_organize_commands_with_duplicates_and_ordering():
    """Test that duplicates are removed and commands are sorted by priority."""
    cmds = [
        CorrectedCommand('cmd1', 10),
        CorrectedCommand('cmd2', 5),
        CorrectedCommand('cmd1', 10),  # duplicate of first
        CorrectedCommand('cmd3', 7),
    ]
    # Convert to an iterator
    result = list(organize_commands(iter(cmds)))
    # First command should be the first element of the input
    assert result[0] == CorrectedCommand('cmd1', 10)
    # Remaining commands should be sorted by priority and without duplicates
    expected = [
        CorrectedCommand('cmd2', 5),
        CorrectedCommand('cmd3', 7),
    ]
    assert result[1:] == expected

def test_organize_commands_empty_iterable():
    """Test that an empty iterable returns no commands."""
    result = list(organize_commands(iter([])))
    assert result == []

def test_organize_commands_single_element():
    """Test that a single command is yielded unchanged."""
    single = CorrectedCommand('only', 42)
    result = list(organize_commands(iter([single])))
    assert result == [single]
