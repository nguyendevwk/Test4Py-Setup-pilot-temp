import pytest
import types
from collections import namedtuple

# Import the target module
import thefuck.corrector as corrector

# Simple CorrectedCommand mock
CorrectedCommand = namedtuple('CorrectedCommand', ['command', 'priority'])

# Dummy Rule class
class DummyRule:
    def __init__(self, match, corrections, priority=0, enabled=True):
        self._match = match
        self._corrections = corrections
        self.priority = priority
        self.is_enabled = enabled

    def is_match(self, cmd):
        return self._match(cmd)

    def get_corrected_commands(self, cmd):
        return [CorrectedCommand(c, self.priority) for c in self._corrections]


def test_get_corrected_commands_normal(monkeypatch):
    # Two rules: one matches, one does not
    rule1 = DummyRule(lambda c: c == 'ls', ['ls -l'], priority=1)
    rule2 = DummyRule(lambda c: False, ['should not appear'], priority=2)
    monkeypatch.setattr(corrector, 'get_rules', lambda: [rule1, rule2])

    # Command that matches rule1
    result = list(corrector.get_corrected_commands('ls'))
    # Should contain only the corrected command from rule1
    assert result == [CorrectedCommand('ls -l', 1)]


def test_get_corrected_commands_organization(monkeypatch):
    # Three rules, two match, produce duplicates and different priorities
    rule1 = DummyRule(lambda c: c == 'git', ['git status'], priority=5)
    rule2 = DummyRule(lambda c: c == 'git', ['git status', 'git commit'], priority=3)
    rule3 = DummyRule(lambda c: False, ['ignored'], priority=1)
    monkeypatch.setattr(corrector, 'get_rules', lambda: [rule1, rule2, rule3])

    result = list(corrector.get_corrected_commands('git'))
    # Expected: first command from rule1 (priority 5), then unique sorted by priority
    expected = [
        CorrectedCommand('git status', 5),          # first
        CorrectedCommand('git status', 3),          # duplicate removed
        CorrectedCommand('git commit', 3)           # unique
    ]
    assert result == expected


def test_get_corrected_commands_no_matches(monkeypatch):
    # Rule that never matches
    rule = DummyRule(lambda c: False, ['never'], priority=1)
    monkeypatch.setattr(corrector, 'get_rules', lambda: [rule])

    result = list(corrector.get_corrected_commands('anything'))
    assert result == []  # generator yields nothing
