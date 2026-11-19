import sys
import importlib
import types
import os
from pathlib import Path
import pytest

# Import the target function after setting up a controlled environment
def _reload_get_rules_import_paths(user_dir, contrib_dirs):
    # Temporarily modify sys.path and settings.user_dir
    original_sys_path = sys.path.copy()
    original_user_dir = None
    try:
        # Ensure the module is reloaded with the new settings
        from thefuck import conf
        original_user_dir = conf.settings.user_dir
        conf.settings.user_dir = Path(user_dir)

        # Insert contrib directories into sys.path
        sys.path = [str(user_dir)] + [str(d) for d in contrib_dirs] + sys.path

        # Reload the module to pick up changes
        import thefuck.corrector
        importlib.reload(thefuck.corrector)
        return thefuck.corrector.get_rules_import_paths
    finally:
        sys.path = original_sys_path
        if original_user_dir is not None:
            conf.settings.user_dir = original_user_dir

@pytest.fixture
def temp_dirs(tmp_path):
    # Create a user rules directory
    user_rules = tmp_path / "user_rules"
    user_rules.mkdir()
    # Create a contrib package with rules
    contrib_pkg = tmp_path / "thefuck_contrib_example"
    contrib_pkg.mkdir()
    (contrib_pkg / "rules").mkdir()
    # Create a contrib package without rules
    contrib_pkg_no_rules = tmp_path / "thefuck_contrib_norules"
    contrib_pkg_no_rules.mkdir()
    return user_rules, contrib_pkg, contrib_pkg_no_rules

def test_bundled_and_user_paths(temp_dirs):
    user_rules, _, _ = temp_dirs
    get_paths = _reload_get_rules_import_paths(user_rules, [])
    paths = list(get_paths())
    # The first path should be the bundled rules directory
    bundled = Path(__file__).parent.parent / "rules"
    assert bundled in paths
    # The second path should be the user rules directory
    assert user_rules in paths
    # No third‑party paths should be present
    assert all(p.parent.name != "thefuck_contrib_example" for p in paths)

def test_third_party_contrib(temp_dirs):
    user_rules, contrib_pkg, _ = temp_dirs
    get_paths = _reload_get_rules_import_paths(user_rules, [contrib_pkg])
    paths = list(get_paths())
    # The contrib rules directory should be included
    assert contrib_pkg / "rules" in paths
    # Ensure the bundled and user paths are still present
    bundled = Path(__file__).parent.parent / "rules"
    assert bundled in paths
    assert user_rules in paths

def test_no_contrib_rules(temp_dirs):
    user_rules, _, contrib_pkg_no_rules = temp_dirs
    get_paths = _reload_get_rules_import_paths(user_rules, [contrib_pkg_no_rules])
    paths = list(get_paths())
    # The contrib package without a rules directory should not be yielded
    assert not any(p.parent.name == "thefuck_contrib_norules" for p in paths)
    # Bundled and user paths should still be present
    bundled = Path(__file__).parent.parent / "rules"
    assert bundled in paths
    assert user_rules in paths
