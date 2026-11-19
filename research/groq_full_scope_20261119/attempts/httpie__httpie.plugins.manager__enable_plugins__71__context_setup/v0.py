import sys
import os
import pytest
from pathlib import Path
from contextlib import nullcontext

from httpie.plugins.manager import enable_plugins, _load_directories


def test_enable_plugins_none_returns_nullcontext():
    """When plugins_dir is None, enable_plugins should return a nullcontext."""
    ctx = enable_plugins(None)
    assert ctx is nullcontext()
    # Using the context manager should not alter sys.path
    original_sys_path = list(sys.path)
    with ctx:
        assert sys.path == original_sys_path


def test_enable_plugins_adds_and_removes_path(tmp_path: Path):
    """enable_plugins should add the given directory to sys.path during the context
    and remove it afterwards."""
    # Create a dummy plugin directory
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    # Ensure the directory is not already in sys.path
    assert str(plugin_dir) not in sys.path

    with enable_plugins(plugin_dir) as ctx:
        # Inside the context, the directory should be present
        assert str(plugin_dir) in sys.path
        # The context manager should yield None
        assert ctx is None

    # After exiting the context, the directory should be removed
    assert str(plugin_dir) not in sys.path


def test_load_directories_yields_and_restores_sys_path(tmp_path: Path):
    """_load_directories should yield control and restore sys.path after exit."""
    # Create two dummy directories
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()

    # Capture original sys.path
    original_sys_path = list(sys.path)

    # Use the generator directly
    gen = _load_directories([dir1, dir2])
    # Before first yield, sys.path should be unchanged
    assert list(sys.path) == original_sys_path

    # Advance to the yield
    next(gen)
    # During the context, both directories should be in sys.path
    assert str(dir1) in sys.path
    assert str(dir2) in sys.path

    # Close the generator to trigger finally block
    gen.close()
    # After cleanup, sys.path should be restored
    assert list(sys.path) == original_sys_path
