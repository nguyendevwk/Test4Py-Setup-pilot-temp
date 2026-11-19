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
    dummy_output = "error: unknown revision 'HEAD' for 'git'"
    dummy_command = DummyCommand(script_parts=["git"], output=dummy_output)

    # Monkeypatch _get_actual_scm to avoid external dependency
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)

    # Act
    result = match(dummy_command)

    # Assert
    assert result is True
    assert "unknown revision" in dummy_command.output
    assert dummy_command.script_parts[0] in wrong_scm_patterns


def test_match_no_pattern(monkeypatch):
    """If the output does not contain the expected pattern, match should return False."""
    # Arrange
    dummy_output = "some unrelated error message"
    dummy_command = DummyCommand(script_parts=["git"], output=dummy_output)

    # Monkeypatch _get_actual_scm to avoid external dependency
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)

    # Act
    result = match(dummy_command)

    # Assert
    assert result is False
    assert dummy_command.script_parts[0] in wrong_scm_patterns
    assert "unknown revision" not in dummy_command.output


def test_match_missing_scm(monkeypatch):
    """If the script_parts[0] is not a known SCM, match should raise a KeyError."""
    # Arrange
    dummy_output = "error: unknown revision 'HEAD' for 'git'"
    dummy_command = DummyCommand(script_parts=["unknown_scm"], output=dummy_output)

    # Monkeypatch _get_actual_scm to avoid external dependency
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)

    # Act & Assert
    with pytest.raises(KeyError):
        match(dummy_command)
