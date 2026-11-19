import pytest
from collections import namedtuple

# Import the target function
from thefuck.corrector import organize_commands

# Define a minimal CorrectedCommand mock with priority and equality
CorrectedCommand = namedtuple('CorrectedCommand', ['command', 'priority'])

def test_organize_commands_normal_and_sorted():
    """Test that commands are yielded sorted by priority and duplicates are removed."""
    cmds = [
        CorrectedCommand('cmd1', 10),
        CorrectedCommand('cmd2', 5),
        CorrectedCommand('cmd3', 20),
    ]
    # Duplicate with same priority as first
    cmds.append(CorrectedCommand('cmd1', 10))

    result = list(organize_commands(iter(cmds)))
    # First command should be the first yielded
    assert result[0] == CorrectedCommand('cmd1', 10)
    # Remaining should be sorted by priority and unique
    assert result[1:] == [CorrectedCommand('cmd2', 5), CorrectedCommand('cmd3', 20)]

def test_organize_commands_empty_iterator():
    """Test that an empty iterator returns no commands."""
    empty_iter = iter([])
    result = list(organize_commands(empty_iter))
    assert result == []

def test_organize_commands_duplicate_removal():
    """Test that duplicate commands are removed based on equality."""
    cmds = [
        CorrectedCommand('cmdA', 1),
        CorrectedCommand('cmdB', 2),
        CorrectedCommand('cmdA', 1),  # duplicate
        CorrectedCommand('cmdC', 3),
        CorrectedCommand('cmdB', 2),  # duplicate
    ]
    result = list(organize_commands(iter(cmds)))
    # Should contain each unique command once, sorted by priority
    expected = [
        CorrectedCommand('cmdA', 1),
        CorrectedCommand('cmdB', 2),
        CorrectedCommand('cmdC', 3),
    ]
    assert result == expected
