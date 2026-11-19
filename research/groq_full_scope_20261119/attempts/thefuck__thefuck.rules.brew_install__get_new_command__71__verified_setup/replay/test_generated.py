import re
import pytest
from types import SimpleNamespace

import thefuck.rules.brew_install as brew_install


def test_get_new_command_replaces_formula(tmp_path):
    # Arrange: create a fake command object with script and output
    cmd = SimpleNamespace(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Monkeypatch the internal helper to return a known similar formula
    brew_install._get_similar_formula = lambda x: "bar"

    # Act
    new_cmd = brew_install.get_new_command(cmd)

    # Assert: the script should have 'foo' replaced by 'bar'
    assert new_cmd == "brew install bar"
    # Ensure the original command is unchanged
    assert cmd.script == "brew install foo"


def test_get_new_command_no_match_raises():
    # Arrange: command output that does not match the regex
    cmd = SimpleNamespace(
        script="brew install foo",
        output="Some unrelated error message\n"
    )
    # Act & Assert: IndexError should be raised because re.findall returns empty list
    with pytest.raises(IndexError):
        brew_install.get_new_command(cmd)


def test_get_new_command_no_change_when_similar_is_same(tmp_path):
    # Arrange: command where the similar formula is the same as the original
    cmd = SimpleNamespace(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    brew_install._get_similar_formula = lambda x: "foo"

    # Act
    new_cmd = brew_install.get_new_command(cmd)

    # Assert: script remains unchanged
    assert new_cmd == "brew install foo"
