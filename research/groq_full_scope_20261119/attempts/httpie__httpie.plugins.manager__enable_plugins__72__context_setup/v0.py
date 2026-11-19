import sys
import pytest
from pathlib import Path
from httpie.plugins.manager import enable_plugins

def test_enable_plugins_adds_and_removes_path(tmp_path: Path):
    # Create a dummy plugin directory
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    # Record original sys.path
    original_sys_path = list(sys.path)
    # Use the context manager
    with enable_plugins(plugin_dir) as cm:
        # Inside the context, the plugin directory should be at the front of sys.path
        assert cm is None  # Context manager returns None
        assert sys.path[0] == str(plugin_dir)
        # Ensure other paths remain unchanged after the new one
        assert sys.path[1:] == original_sys_path
    # After exiting, the path should be removed
    assert str(plugin_dir) not in sys.path
    assert sys.path == original_sys_path

def test_enable_plugins_none_returns_nullcontext():
    # When plugins_dir is None, the context manager should be a nullcontext
    ctx = enable_plugins(None)
    # The returned object should be an instance of contextlib.nullcontext
    from contextlib import nullcontext
    assert isinstance(ctx, nullcontext)
    # Entering and exiting should not alter sys.path
    original_sys_path = list(sys.path)
    with ctx:
        assert sys.path == original_sys_path
    assert sys.path == original_sys_path

def test_enable_plugins_with_nonexistent_directory(tmp_path: Path):
    # Provide a path that does not exist; get_site_paths will still return it
    nonexistent_dir = tmp_path / "does_not_exist"
    # Record original sys.path
    original_sys_path = list(sys.path)
    with enable_plugins(nonexistent_dir):
        # The nonexistent directory should still be added to sys.path
        assert str(nonexistent_dir) == sys.path[0]
    # After exiting, it should be removed
    assert str(nonexistent_dir) not in sys.path
    assert sys.path == original_sys_path
