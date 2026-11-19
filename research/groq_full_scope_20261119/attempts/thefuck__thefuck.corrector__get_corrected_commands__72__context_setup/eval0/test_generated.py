import importlib
import sys
import types
import pathlib
import pytest

# Import the target module
import thefuck.corrector as corrector

# Helper to create a minimal rule file
def create_rule_file(tmp_path, name, match_text, corrected_text, priority=0, enabled=True):
    rule_dir = tmp_path / "rules"
    rule_dir.mkdir()
    rule_file = rule_dir / f"{name}.py"
    rule_file.write_text(f"""
from thefuck.types import Rule, CorrectedCommand, Command

class {name.capitalize()}Rule(Rule):
    priority = {priority}
    is_enabled = {enabled}

    def is_match(self, command):
        return command.text == "{match_text}"

    def get_corrected_commands(self, command):
        yield CorrectedCommand(command, "{corrected_text}", priority={priority})
""")
    return rule_file

# Patch settings.user_dir to point to tmp_path
@pytest.fixture
def patch_settings(tmp_path):
    original = corrector.settings.user_dir
    corrector.settings.user_dir = tmp_path
    yield
    corrector.settings.user_dir = original

# Patch get_rules_import_paths to yield only our temp rules directory
@pytest.fixture
def patch_get_rules_import_paths(tmp_path):
    original = corrector.get_rules_import_paths
    def fake():
        yield tmp_path / "rules"
    corrector.get_rules_import_paths = fake
    yield
    corrector.get_rules_import_paths = original

# Reload the module after patches
@pytest.fixture(autouse=True)
def reload_module():
    importlib.reload(corrector)

# Test normal behavior: a rule matches and returns a corrected command
def test_get_corrected_commands_normal(tmp_path, patch_settings, patch_get_rules_import_paths):
    rule_file = create_rule_file(tmp_path, "echo", "echo foo", "echo bar", priority=10)
    # Create a dummy Command
    cmd = types.SimpleNamespace(text="echo foo", priority=0)
    # Call the function
    corrected = list(corrector.get_corrected_commands(cmd))
    assert len(corrected) == 1
    assert corrected[0].command.text == "echo foo"
    assert corrected[0].text == "echo bar"
    assert corrected[0].priority == 10

# Test boundary: no rules match, generator should be empty
def test_get_corrected_commands_no_match(tmp_path, patch_settings, patch_get_rules_import_paths):
    create_rule_file(tmp_path, "ls", "ls -l", "ls -a", priority=5)
    cmd = types.SimpleNamespace(text="echo foo", priority=0)
    corrected = list(corrector.get_corrected_commands(cmd))
    assert corrected == []

# Test error: rule raises exception during is_match, should be ignored and not crash
def test_get_corrected_commands_rule_error(tmp_path, patch_settings, patch_get_rules_import_paths):
    rule_dir = tmp_path / "rules"
    rule_dir.mkdir()
    rule_file = rule_dir / "bad.py"
    rule_file.write_text("""
from thefuck.types import Rule, CorrectedCommand, Command

class BadRule(Rule):
    priority = 1
    is_enabled = True

    def is_match(self, command):
        raise ValueError("intentional error")

    def get_corrected_commands(self, command):
        yield CorrectedCommand(command, "bad", priority=1)
""")
    cmd = types.SimpleNamespace(text="anything", priority=0)
    corrected = list(corrector.get_corrected_commands(cmd))
    # No corrected commands should be returned because the rule errors out
    assert corrected == []
