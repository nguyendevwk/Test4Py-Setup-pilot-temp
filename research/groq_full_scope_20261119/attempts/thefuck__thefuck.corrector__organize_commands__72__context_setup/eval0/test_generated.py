import pytest
from collections import namedtuple

# Import the function under test
from thefuck.corrector import organize_commands

# Define a minimal CorrectedCommand mock with priority and equality
CorrectedCommand = namedtuple('CorrectedCommand', ['command', 'priority'])

def test_organize_commands_removes_duplicates_and_sorts():
    """Test that duplicates are removed and commands are sorted by priority."""
    cmds = [
        CorrectedCommand('cmd1', 10),
        CorrectedCommand('cmd2', 5),
        CorrectedCommand('cmd1', 10),  # duplicate
        CorrectedCommand('cmd3', 7),
    ]
    # Create an iterator
    iterator = iter(cmds)
    result = list(organize_commands(iterator))
    # Expected order: first command (cmd1,10), then cmd2 (5), then cmd3 (7)
    expected = [
        CorrectedCommand('cmd1', 10),
        CorrectedCommand('cmd2', 5),
        CorrectedCommand('cmd3', 7),
    ]
    assert result == expected, f"Expected {expected}, got {result}"

def test_organize_commands_empty_iterable_returns_nothing():
    """Test that an empty iterable yields nothing."""
    iterator = iter([])
    result = list(organize_commands(iterator))
    assert result == [], f"Expected empty list, got {result}"

def test_organize_commands_single_element():
    """Test that a single element is yielded unchanged."""
    cmd = CorrectedCommand('only', 42)
    iterator = iter([cmd])
    result = list(organize_commands(iterator))
    assert result == [cmd], f"Expected [{cmd}], got {result}"
