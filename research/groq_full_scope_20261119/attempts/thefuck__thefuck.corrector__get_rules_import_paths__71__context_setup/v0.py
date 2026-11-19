import sys
import types
import importlib
import pathlib
import pytest

# Import the target function after ensuring the package is importable
from thefuck.corrector import get_rules_import_paths
from thefuck import conf

@pytest.fixture
def monkeypatch_settings(monkeypatch, tmp_path):
    """Monkeypatch settings.user_dir to a temporary directory."""
    monkeypatch.setattr(conf.settings, "user_dir", tmp_path)
    return tmp_path

def test_bundled_and_user_paths(monkeypatch_settings):
    """Ensure the bundled rules directory and the user rules directory are yielded."""
    # The bundled rules path is relative to this module's file
    bundled = pathlib.Path(__file__).parent.parent.joinpath("rules")
    user_dir = monkeypatch_settings.joinpath("rules")
    # Create the user rules directory to avoid errors
    user_dir.mkdir(parents=True, exist_ok=True)

    paths = list(get_rules_import_paths())
    # The first two yielded paths should match bundled and user_dir
    assert paths[0] == bundled
    assert paths[1] == user_dir

def test_third_party_rules(monkeypatch, tmp_path):
    """Verify that third‑party contrib modules are discovered."""
    # Create a fake third‑party module directory in a temporary sys.path entry
    contrib_dir = tmp_path / "thefuck_contrib_example"
    contrib_dir.mkdir()
    rules_dir = contrib_dir / "rules"
    rules_dir.mkdir()
    # Add the temporary directory to sys.path
    monkeypatch.setitem(sys.modules, "__path__", [str(tmp_path)])
    original_sys_path = sys.path[:]
    sys.path.insert(0, str(tmp_path))
    try:
        paths = list(get_rules_import_paths())
        # The third yielded path should be the rules directory of the contrib module
        assert rules_dir in paths
    finally:
        sys.path[:] = original_sys_path

def test_no_contrib(monkeypatch):
    """When no contrib modules exist, only bundled and user paths are yielded."""
    # Ensure sys.path has no contrib modules
    original_sys_path = sys.path[:]
    sys.path[:] = ["/nonexistent/path"]
    try:
        paths = list(get_rules_import_paths())
        # Only two paths should be yielded
        assert len(paths) == 2
        # They should be the bundled and user directories
        bundled = pathlib.Path(__file__).parent.parent.joinpath("rules")
        user_dir = conf.settings.user_dir.joinpath("rules")
        assert paths[0] == bundled
        assert paths[1] == user_dir
    finally:
        sys.path[:] = original_sys_path
