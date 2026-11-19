import re
import pytest
from thefuck.rules.brew_install import get_new_command, _get_similar_formula
from thefuck.utils import replace_argument


class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output


def test_get_new_command_replaces_formula(monkeypatch, tmp_path):
    # Arrange: patch _get_similar_formula to return a predictable value
    monkeypatch.setattr(
        "thefuck.rules.brew_install._get_similar_formula",
        lambda x: "bar",
    )
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\nSome other text",
    )

    # Act
    new_cmd = get_new_command(cmd)

    # Assert
    assert new_cmd == "brew install bar"
    # Ensure the replacement only affected the formula part
    assert "foo" not in new_cmd
    assert "bar" in new_cmd


def test_get_new_command_uses_first_error_in_output(monkeypatch):
    # Arrange: patch _get_similar_formula to return a predictable value
    monkeypatch.setattr(
        "thefuck.rules.brew_install._get_similar_formula",
        lambda x: "baz",
    )
    output = (
        "Error: No available formula for alpha\n"
        "Error: No available formula for beta\n"
    )
    cmd = DummyCommand(
        script="brew install alpha",
        output=output,
    )

    # Act
    new_cmd = get_new_command(cmd)

    # Assert: only the first formula is replaced
    assert new_cmd == "brew install baz"
    assert "alpha" not in new_cmd
    assert "beta" in output  # original output remains unchanged


def test_get_new_command_raises_index_error_when_no_match():
    # Arrange: command output without the expected error pattern
    cmd = DummyCommand(
        script="brew install foo",
        output="Some unrelated error message",
    )

    # Act & Assert: accessing the first match should raise IndexError
    with pytest.raises(IndexError):
        get_new_command(cmd)
