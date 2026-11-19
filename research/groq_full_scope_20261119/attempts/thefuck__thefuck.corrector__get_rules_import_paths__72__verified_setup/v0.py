import sys
import types
from pathlib import Path
import pytest

# Import the target function after setting up a minimal environment
from thefuck.corrector import get_rules_import_paths
from thefuck import settings

@pytest.fixture
def reset_sys_path(monkeypatch):
    original = sys.path[:]
    monkeypatch.setattr(sys, "path", original)
    yield
    sys.path[:] = original

def test_bundled_rules_path(tmp_path, reset_sys_path):
    # The bundled rules directory should always be yielded
    bundled = Path(__file__).parent.parent.joinpath("rules")
    paths = list(get_rules_import_paths())
    assert bundled in paths, f"Bundled path {bundled} not in yielded paths {paths}"

def test_user_dir_rules_path(tmp_path, reset_sys_path, monkeypatch):
    # Create a fake user directory with a rules subdirectory
    user_dir = tmp_path / "user"
    rules_dir = user_dir / "rules"
    rules_dir.mkdir(parents=True)
    monkeypatch.setattr(settings, "user_dir", user_dir)
    paths = list(get_rules_import_paths())
    assert rules_dir in paths, f"User rules path {rules_dir} not in yielded paths {paths}"

def test_contrib_module_rules_path(tmp_path, reset_sys_path, monkeypatch):
    # Create a fake contrib module in sys.path
    contrib_dir = tmp_path / "thefuck_contrib_example"
    contrib_dir.mkdir()
    contrib_rules = contrib_dir / "rules"
    contrib_rules.mkdir()
    # Add the parent of contrib_dir to sys.path
    monkeypatch.setitem(sys.path, 0, str(tmp_path))
    paths = list(get_rules_import_paths())
    assert contrib_rules in paths, f"Contrib rules path {contrib_rules} not in yielded paths {paths}"
