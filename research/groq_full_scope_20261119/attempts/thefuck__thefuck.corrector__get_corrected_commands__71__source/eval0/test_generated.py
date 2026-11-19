import pytest
from thefuck.corrector import get_corrected_commands, organize_commands, get_rules
from thefuck.types import Command, CorrectedCommand

# Helper classes to simulate rules
class DummyRule:
    def __init__(self, match, outputs):
        self._match = match
        self._outputs = outputs

    def is_match(self, command):
        return self._match

    def get_corrected_commands(self, command):
        for out in self._outputs:
            yield CorrectedCommand(out, command)


def test_get_corrected_commands_dedup_and_sort(monkeypatch, tmp_path):
    # Prepare a command
    cmd = Command("echo hello", tmp_path, None, None)

    # Two rules: one matches, one does not
    rule1 = DummyRule(True, ["echo hi", "echo hello"])
    rule2 = DummyRule(False, ["echo bye"])

    # Patch get_rules to return our dummy rules
    monkeypatch.setattr("thefuck.corrector.get_rules", lambda: [rule1, rule2])

    # Patch organize_commands to simply return a list for easier inspection
    monkeypatch.setattr("thefuck.corrector.organize_commands", lambda cmds: list(cmds))

    # Call the function
    result = get_corrected_commands(cmd)

    # Expected unique sorted commands: "echo hello" and "echo hi"
    expected = [CorrectedCommand("echo hello", cmd), CorrectedCommand("echo hi", cmd)]
    assert result == expected


def test_get_corrected_commands_empty(monkeypatch, tmp_path):
    cmd = Command("ls", tmp_path, None, None)

    # No rules match
    rule = DummyRule(False, ["ls -l"])
    monkeypatch.setattr("thefuck.corrector.get_rules", lambda: [rule])
    monkeypatch.setattr("thefuck.corrector.organize_commands", lambda cmds: list(cmds))

    result = get_corrected_commands(cmd)
    assert result == []


def test_get_corrected_commands_rule_exception(monkeypatch, tmp_path):
    cmd = Command("cat file", tmp_path, None, None)

    # Rule that raises an exception during get_corrected_commands
    class BadRule:
        def is_match(self, command):
            return True

        def get_corrected_commands(self, command):
            raise RuntimeError("unexpected error")

    monkeypatch.setattr("thefuck.corrector.get_rules", lambda: [BadRule()])
    monkeypatch.setattr("thefuck.corrector.organize_commands", lambda cmds: list(cmds))

    with pytest.raises(RuntimeError, match="unexpected error"):
        list(get_corrected_commands(cmd))
