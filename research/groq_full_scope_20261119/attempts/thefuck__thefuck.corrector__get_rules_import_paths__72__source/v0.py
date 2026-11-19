import importlib
import sys
import types
import pytest
from pathlib import Path as PyPath

# Import the module under test
from thefuck.corrector import get_rules_import_paths
from thefuck.system import Path

@pytest.fixture
def reload_module(tmp_path):
    """Reload the module with a fresh settings.user_dir."""
    # Monkeypatch settings.user_dir to a temporary directory
    import thefuck.conf.settings as settings
    original_user_dir = settings.user_dir
    settings.user_dir = tmp_path
    # Reload the module to pick up the new settings
    import thefuck.corrector as mod
    importlib.reload(mod)
    yield mod
    # Restore original settings
    settings.user_dir = original_user_dir
    importlib.reload(mod)

def test_bundled_rules_path(reload_module, tmp_path):
    """The bundled rules directory should be yielded."""
    mod = reload_module
    # The bundled path is relative to the module file
    bundled = Path(mod.__file__).parent.joinpath('rules')
    paths = list(mod.get_rules_import_paths())
    assert bundled in paths, f"Bundled path {bundled} not in {paths}"

def test_user_rules_path(reload_module, tmp_path):
    """The user rules directory should be yielded."""
    mod = reload_module
    user_rules = tmp_path.joinpath('rules')
    user_rules.mkdir()
    paths = list(mod.get_rules_import_paths())
    assert user_rules in paths, f"User path {user_rules} not in {paths}"

def test_contrib_rules_paths(reload_module, tmp_path):
    """Contrib modules with a 'rules' subdirectory should be yielded."""
    mod = reload_module
    # Create a fake contrib module directory in a temporary sys.path entry
    contrib_dir = tmp_path / "thefuck_contrib_example"
    contrib_dir.mkdir()
    rules_dir = contrib_dir / "rules"
    rules_dir.mkdir()
    # Add the temporary directory to sys.path
    original_sys_path = sys.path.copy()
    sys.path.insert(0, str(tmp_path))
    try:
        paths = list(mod.get_rules_import_paths())
        assert rules_dir in paths, f"Contrib rules {rules_dir} not in {paths}"
    finally:
        sys.path = original_sys_path
