import pytest
from thefuck.rules.scm_correction import match, wrong_scm_patterns, _get_actual_scm


class DummyCommand:
    def __init__(self, script_parts, output):
        self.script_parts = script_parts
        self.output = output


def test_match_success(monkeypatch):
    """When the output contains the expected pattern and _get_actual_scm returns True,
    match should return True."""
    # Arrange
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)
    cmd = DummyCommand(script_parts=["git"], output="fatal: not a git repository")
    pattern = wrong_scm_patterns["git"]
    # Act
    result = match(cmd)
    # Assert
    assert result is True
    assert pattern in cmd.output


def test_match_no_pattern(monkeypatch):
    """If the output does not contain the pattern, match should return False."""
    # Arrange
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)
    cmd = DummyCommand(script_parts=["git"], output="some unrelated error")
    # Act
    result = match(cmd)
    # Assert
    assert result is False


def test_match_missing_scm(monkeypatch):
    """If the command's first part is not a known SCM, match should raise KeyError."""
    # Arrange
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)
    cmd = DummyCommand(script_parts=["unknown_scm"], output="some error")
    # Act & Assert
    with pytest.raises(KeyError):
        match(cmd)
