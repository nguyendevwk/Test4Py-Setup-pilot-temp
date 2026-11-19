import pytest
from thefuck.corrector import organize_commands

class DummyCommand:
    def __init__(self, cmd, priority):
        self.cmd = cmd
        self.priority = priority

    def __repr__(self):
        return f"<DummyCommand {self.cmd!r} p={self.priority}>"

    def __eq__(self, other):
        return isinstance(other, DummyCommand) and self.cmd == other.cmd and self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

def test_organize_commands_removes_duplicates_and_sorts():
    # Commands with varying priorities and a duplicate
    cmds = [
        DummyCommand("cmd1", 10),
        DummyCommand("cmd2", 5),
        DummyCommand("cmd1", 10),  # duplicate
        DummyCommand("cmd3", 7),
    ]
    # Convert to iterator
    result = list(organize_commands(iter(cmds)))
    # First command should be the first in the original iterable
    assert result[0] == DummyCommand("cmd1", 10)
    # Remaining commands should be sorted by priority and without duplicates
    expected = [
        DummyCommand("cmd2", 5),
        DummyCommand("cmd3", 7),
    ]
    assert result[1:] == expected

def test_organize_commands_empty_iterable_returns_nothing():
    # Empty iterable should yield nothing
    result = list(organize_commands(iter([])))
    assert result == []

def test_organize_commands_single_command_yields_itself():
    # Single command should be yielded as the only element
    cmd = DummyCommand("only", 42)
    result = list(organize_commands(iter([cmd])))
    assert result == [cmd]
