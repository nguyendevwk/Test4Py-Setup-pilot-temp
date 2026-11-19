import pytest
from thefuck.rules.scm_correction import match, wrong_scm_patterns, _get_actual_scm


class DummyCommand:
    def __init__(self, script_parts, output):
        self.script_parts = script_parts
        self.output = output


def test_match_returns_true_when_pattern_and_actual_scm(monkeypatch):
    """match should return True when the output contains the wrong SCM pattern
    and the actual SCM is detected."""
    # Pick a known SCM key from the patterns dictionary
    scm_key = next(iter(wrong_scm_patterns))
    pattern = wrong_scm_patterns[scm_key]
    cmd = DummyCommand([scm_key, "commit"], f"Error: {pattern} detected")
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)
    assert match(cmd) is True


def test_match_returns_false_when_pattern_not_in_output(monkeypatch):
    """match should return False when the output does not contain the wrong SCM pattern."""
    scm_key = next(iter(wrong_scm_patterns))
    cmd = DummyCommand([scm_key, "commit"], "All good, no errors")
    monkeypatch.setattr("thefuck.rules.scm_correction._get_actual_scm", lambda: True)
    assert match(cmd) is False


def test_match_raises_key_error_for_unknown_scm():
    """match should raise a KeyError when the command's first part is not a known SCM."""
    cmd = DummyCommand(["unknown_scm", "commit"], "Some output")
    with pytest.raises(KeyError):
        match(cmd)
