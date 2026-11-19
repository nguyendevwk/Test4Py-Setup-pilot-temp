import sys
import os
import warnings
from pathlib import Path
import pytest
from httpie.plugins.manager import enable_plugins

def test_enable_plugins_with_none_returns_nullcontext():
    """When None is passed, enable_plugins should return a nullcontext."""
    ctx = enable_plugins(None)
    # nullcontext is a context manager that yields None
    with ctx as value:
        assert value is None

def test_enable_plugins_with_existing_directory_context_manager(tmp_path: Path):
    """When a valid directory is passed, enable_plugins should return a usable context manager."""
    # Create a dummy directory that would be considered a plugin directory
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    ctx = enable_plugins(plugin_dir)
    # The context manager should be enterable and yield None
    with ctx as value:
        assert value is None

def test_enable_plugins_with_nonexistent_directory(tmp_path: Path):
    """When a non-existent directory is passed, enable_plugins should still return a context manager that can be entered."""
    nonexistent_dir = tmp_path / "does_not_exist"
    # Ensure the directory does not exist
    assert not nonexistent_dir.exists()
    ctx = enable_plugins(nonexistent_dir)
    # The context manager should be enterable and yield None even if the path is missing
    with ctx as value:
        assert value is None
