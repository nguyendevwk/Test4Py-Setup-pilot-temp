import os
import re
import pytest
from thefuck.rules.brew_install import get_new_command, _get_similar_formula
from thefuck.specific.brew import get_brew_path_prefix, brew_available

class DummyCommand:
    def __init__(self, script, output):
        self.script = script
        self.output = output

def _setup_brew_prefix(tmp_path, formulas):
    """Create a fake brew prefix with given formula names."""
    brew_prefix = tmp_path / "Cellar"
    brew_prefix.mkdir(parents=True)
    for name in formulas:
        (brew_prefix / f"{name}.rb").write_text("# dummy formula")
    os.environ["BREW_PREFIX"] = str(tmp_path)
    return brew_prefix

def test_get_new_command_replaces_formula(tmp_path):
    # Arrange: fake brew prefix with one available formula "bar"
    _setup_brew_prefix(tmp_path, ["bar"])
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act
    new_cmd = get_new_command(cmd)
    # Assert: "foo" replaced by "bar"
    assert new_cmd == "brew install bar"

def test_get_new_command_raises_on_no_match(tmp_path):
    # Arrange: fake brew prefix with no formulas
    _setup_brew_prefix(tmp_path, [])
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act & Assert: IndexError from re.findall or ValueError from _get_similar_formula
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_selects_closest_formula(tmp_path):
    # Arrange: fake brew prefix with two formulas "bar" and "baz"
    _setup_brew_prefix(tmp_path, ["bar", "baz"])
    cmd = DummyCommand(
        script="brew install foo",
        output="Error: No available formula for foo\n"
    )
    # Act
    new_cmd = get_new_command(cmd)
    # Assert: "foo" replaced by the closest formula, which should be "bar"
    assert new_cmd == "brew install bar"
