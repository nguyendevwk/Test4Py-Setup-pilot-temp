import re
import os
import sys
import types
import importlib
import pytest

# Import the target function
from thefuck.rules.brew_install import get_new_command

# Helper class to mimic the command object used by thefuck
class DummyCommand:
    def __init__(self, script: str, output: str):
        self.script = script
        self.output = output

def test_get_new_command_no_match_raises_index_error():
    """
    When the command output does not contain the expected error pattern,
    get_new_command should raise an IndexError due to the regex lookup.
    """
    cmd = DummyCommand(script="brew install foo", output="Some unrelated output")
    with pytest.raises(IndexError):
        get_new_command(cmd)

def test_get_new_command_replaces_formula(tmp_path):
    """
    When the command output contains a missing formula error, get_new_command
    should replace the missing formula with a similar one.  We monkey‑patch
    the helper functions used by the rule to avoid depending on the real
    Homebrew installation.
    """
    # Create a dummy brew environment
    brew_script = tmp_path / "brew"
    brew_script.write_text("#!/usr/bin/env bash\n")
    brew_script.chmod(0o755)

    # Temporarily prepend the dummy brew to PATH
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = f"{tmp_path}:{original_path}"

    # Monkey‑patch helper functions in the module
    module = importlib.import_module("thefuck.rules.brew_install")
    original_get_brew_path_prefix = module.get_brew_path_prefix
    original_brew_available = module.brew_available
    original_get_closest = module.get_closest
    original_replace_argument = module.replace_argument

    try:
        module.get_brew_path_prefix = lambda: ""
        module.brew_available = lambda: True
        module.get_closest = lambda term, prefix: "foo-bar"
        module.replace_argument = lambda script, old, new: script.replace(old, new)

        cmd = DummyCommand(
            script="brew install foo",
            output="Error: No available formula for foo"
        )
        new_cmd = get_new_command(cmd)
        assert new_cmd == "brew install foo-bar"
    finally:
        # Restore original functions and PATH
        module.get_brew_path_prefix = original_get_brew_path_prefix
        module.brew_available = original_brew_available
        module.get_closest = original_get_closest
        module.replace_argument = original_replace_argument
        os.environ["PATH"] = original_path

def test_get_new_command_regex_extraction():
    """
    Verify that the regex used in get_new_command correctly extracts the
    missing formula name from the command output.
    """
    output = "Error: No available formula for abc"
    match = re.findall(r'Error: No available formula for ([a-z]+)', output)
    assert match == ["abc"]
