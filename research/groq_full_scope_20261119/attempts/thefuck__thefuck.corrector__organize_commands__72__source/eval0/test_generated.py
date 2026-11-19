import pytest
from thefuck.corrector import organize_commands
from thefuck.types import CorrectedCommand


class DummyCommand(CorrectedCommand):
    def __init__(self, command, priority):
        self.command = command
        self.priority = priority

    def __repr__(self):
        return f"<DummyCommand {self.command!r} p={self.priority}>"


def test_organize_commands_removes_duplicates_and_sorts():
    cmds = [
        DummyCommand("echo a", 2),
        DummyCommand("echo b", 1),
        DummyCommand("echo a", 2),  # duplicate
        DummyCommand("echo c", 3),
    ]
    result = list(organize_commands(iter(cmds)))
    # First command should be the first in the original iterable
    assert result[0].command == "echo a"
    # Remaining commands sorted by priority and without duplicates
    assert [c.command for c in result[1:]] == ["echo b", "echo c"]
    # No duplicate of "echo a" after the first
    assert all(c.command != "echo a" for c in result[1:])


def test_organize_commands_empty_iterable_returns_nothing():
    result = list(organize_commands(iter([])))
    assert result == []


def test_organize_commands_single_command_yields_it():
    single = [DummyCommand("single", 5)]
    result = list(organize_commands(iter(single)))
    assert result == single
