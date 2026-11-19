import os
import re
import tempfile
import shutil
import pytest
from types import SimpleNamespace

# Import the target module
import thefuck.rules.brew_install as brew_install


def test_get_new_command_replaces_formula(tmp_path):
    # Create a fake brew formula directory with a single formula file
    brew_dir = tmp_path / "Homebrew"
    brew_dir.mkdir()
    formula_dir = brew_dir / "Library/Formula"
    formula_dir.mkdir(parents=True)
    (formula_dir / "myformula.rb").write_text("# dummy formula")

    # Monkeypatch the helper to return our fake brew path
    original_get_brew_path_prefix = brew_install.get_brew_path_prefix
    brew_install.get_brew_path_prefix = lambda: str(brew_dir)

    # Monkeypatch get_closest to return a known similar formula
    original_get_closest = brew_install.get_closest
    brew_install.get_closest = lambda name, formulas, cutoff: "myformula"

    # Prepare a command that triggers the rule
    cmd = SimpleNamespace(
        script="brew install abc",
        output="Error: No available formula for abc\n"
    )

    # Execute the rule
    new_cmd = brew_install.get_new_command(cmd)

    # Verify that the formula name was replaced correctly
    assert new_cmd == "brew install myformula"

    # Restore original functions
    brew_install.get_brew_path_prefix = original_get_brew_path_prefix
    brew_install.get_closest = original_get_closest


def test_get_new_command_no_formula_files(tmp_path):
    # Create an empty brew formula directory
    brew_dir = tmp_path / "Homebrew"
    brew_dir.mkdir()
    formula_dir = brew_dir / "Library/Formula"
    formula_dir.mkdir(parents=True)

    # Monkeypatch the helper to return our fake brew path
    original_get_brew_path_prefix = brew_install.get_brew_path_prefix
    brew_install.get_brew_path_prefix = lambda: str(brew_dir)

    # Monkeypatch get_closest to return None when no formulas exist
    original_get_closest = brew_install.get_closest
    brew_install.get_closest = lambda name, formulas, cutoff: None

    # Prepare a command that triggers the rule
    cmd = SimpleNamespace(
        script="brew install abc",
        output="Error: No available formula for abc\n"
    )

    # Execute the rule; since no similar formula is found, replace_argument
    # should leave the script unchanged
    new_cmd = brew_install.get_new_command(cmd)

    assert new_cmd == "brew install abc"

    # Restore original functions
    brew_install.get_brew_path_prefix = original_get_brew_path_prefix
    brew_install.get_closest = original_get_closest


def test_get_new_command_no_match_raises():
    # Prepare a command with output that does not match the regex
    cmd = SimpleNamespace(
        script="brew install abc",
        output="Some unrelated error message\n"
    )

    # The function should raise an IndexError because re.findall returns empty list
    with pytest.raises(IndexError):
        brew_install.get_new_command(cmd)
