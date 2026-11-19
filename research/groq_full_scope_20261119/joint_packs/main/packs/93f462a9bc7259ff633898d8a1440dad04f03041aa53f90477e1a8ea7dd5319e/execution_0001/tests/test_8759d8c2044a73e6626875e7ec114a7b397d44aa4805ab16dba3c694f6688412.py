import sys
import os
import warnings
from pathlib import Path
import pytest
from contextlib import nullcontext

from httpie.plugins.manager import enable_plugins

def test_enable_plugins_with_none_returns_nullcontext():
    """When plugins_dir is None, enable_plugins should return a nullcontext."""
    ctx = enable_plugins(None)
    assert isinstance(ctx, nullcontext), "Expected nullcontext for None input"
    # Entering and exiting the context should be a no‑op
    with ctx:
        pass

def test_enable_plugins_with_valid_directory_returns_non_null_context(tmp_path: Path):
    """When plugins_dir is a valid Path, enable_plugins should return a context manager
    that is not a nullcontext and can be entered without error."""
    # Create a temporary directory that will act as the plugins directory
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    ctx = enable_plugins(plugins_dir)
    assert not isinstance(ctx, nullcontext), "Expected a non‑nullcontext for a valid directory"
    # Entering the context should not raise any exception
    with ctx:
        pass

def test_enable_plugins_with_nonexistent_directory(tmp_path: Path):
    """When plugins_dir points to a non‑existent directory, enable_plugins should still
    return a context manager that can be entered without raising an exception."""
    # Path that does not exist
    nonexistent_dir = tmp_path / "does_not_exist"
    ctx = enable_plugins(nonexistent_dir)
    # The returned context manager should not be nullcontext
    assert not isinstance(ctx, nullcontext), "Expected a non‑nullcontext for a nonexistent directory"
    # Entering the context should not raise
    with ctx:
        pass
