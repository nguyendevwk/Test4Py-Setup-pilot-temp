import sys
import types
from pathlib import Path
import pytest

# Import the target function and related objects
from thefuck.corrector import get_rules_import_paths
from thefuck.conf import settings

@pytest.fixture
def reset_sys_path(tmp_path):
    """Restore original sys.path after test."""
    original = sys.path[:]
    yield
    sys.path[:] = original

def test_bundled_rules_path(tmp_path, reset_sys_path):
    # Ensure the bundled rules path is yielded
    bundled = Path(__file__).parent.parent.joinpath('thefuck', 'corrector', 'rules')
    paths = list(get_rules_import_paths())
    assert bundled in paths, f"Bundled path {bundled} not in yielded paths {paths}"

def test_user_dir_path(tmp_path, reset_sys_path):
    # Set a fake user directory and check it is yielded
    fake_user_dir = tmp_path / "user_dir"
    fake_user_dir.mkdir()
    settings.user_dir = fake_user_dir
    paths = list(get_rules_import_paths())
    expected = fake_user_dir / "rules"
    assert expected in paths, f"User rules path {expected} not in yielded paths {paths}"

def test_contrib_module_paths(tmp_path, reset_sys_path):
    # Create a fake contrib module in sys.path
    contrib_dir = tmp_path / "thefuck_contrib_example"
    contrib_dir.mkdir()
    rules_dir = contrib_dir / "rules"
    rules_dir.mkdir()
    # Add the tmp_path to sys.path so the module is discoverable
    sys.path.insert(0, str(tmp_path))
    paths = list(get_rules_import_paths())
    assert rules_dir in paths, f"Contrib rules path {rules_dir} not in yielded paths {paths}"
