import pytest
from collections import namedtuple

# Import the function under test
from thefuck.corrector import organize_commands

# Define a minimal CorrectedCommand mock with priority and equality
CorrectedCommand = namedtuple('CorrectedCommand', ['command', 'priority'])

def test_organize_commands_removes_duplicates_and_sorts():
    """
    Verify that organize_commands yields commands sorted by priority
    and removes duplicates (commands with the same priority and command string).
    """
    cmds = [
        CorrectedCommand('echo a', 10),
        CorrectedCommand('echo b', 5),
        CorrectedCommand('echo a', 10),  # duplicate of first
        CorrectedCommand('echo c', 7),
    ]
    # Convert to iterator
    result = list(organize_commands(iter(cmds)))
    # Expected order: first command (echo a, 10), then echo c (7), then echo b (5)
    expected = [
        CorrectedCommand('echo a', 10),
        CorrectedCommand('echo c', 7),
        CorrectedCommand('echo b', 5),
    ]
    assert result == expected, f"Expected {expected}, got {result}"

def test_organize_commands_empty_iterable_returns_nothing():
    """
    Verify that an empty iterable results in no output and no exception.
    """
    empty_iter = iter([])
    result = list(organize_commands(empty_iter))
    assert result == [], "Expected empty list for empty input"

def test_organize_commands_invalid_input_raises_type_error():
    """
    Verify that passing a non-iterable (e.g., None) raises a TypeError.
    """
    with pytest.raises(TypeError):
        list(organize_commands(None))
