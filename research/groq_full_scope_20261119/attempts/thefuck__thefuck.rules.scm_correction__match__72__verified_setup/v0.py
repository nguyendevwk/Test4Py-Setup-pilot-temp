import builtins
import types
import pytest
from types import SimpleNamespace

# Import the target module
import thefuck.rules.scm_correction as scm_correction


def test_match_returns_true_when_pattern_and_actual_scm(monkeypatch):
    """
    Normal case: the command output contains the wrong SCM pattern and
    _get_actual_scm returns True. The match function should return True.
    """
    # Prepare a command with a known SCM and output containing its pattern
    command = SimpleNamespace(
        script_parts=["git"],
        output="fatal: not a git repository (or any of the parent directories): .git"
    )

    # Ensure the pattern for 'git' is present in the output
    pattern = scm_correction.wrong_scm_patterns["git"]
    assert pattern in command.output

    # Monkeypatch _get_actual_scm to return True
    monkeypatch.setattr(scm_correction, "_get_actual_scm", lambda: True)

    assert scm_correction.match(command) is True


def test_match_returns_false_when_pattern_missing(monkeypatch):
    """
    Boundary case: the command output does not contain the wrong SCM pattern.
    The match function should return False regardless of _get_actual_scm.
    """
    command = SimpleNamespace(
        script_parts=["svn"],
        output="some unrelated error message"
    )

    # Monkeypatch _get_actual_scm to return True to ensure it doesn't affect the result
    monkeypatch.setattr(scm_correction, "_get_actual_scm", lambda: True)

    assert scm_correction.match(command) is False


def test_match_raises_key_error_for_unknown_scm():
    """
    Error case: the first script part is not a known SCM key in wrong_scm_patterns.
    Accessing the dictionary should raise a KeyError.
    """
    command = SimpleNamespace(
        script_parts=["unknown_scm"],
        output="some error message"
    )

    with pytest.raises(KeyError):
        scm_correction.match(command)
