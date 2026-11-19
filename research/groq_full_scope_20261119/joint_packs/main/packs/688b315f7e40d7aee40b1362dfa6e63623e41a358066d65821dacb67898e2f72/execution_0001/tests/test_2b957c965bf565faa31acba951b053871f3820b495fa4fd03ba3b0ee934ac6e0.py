import sys
import os
import warnings
import pytest
from pathlib import Path
from contextlib import nullcontext

# Import the target function
from httpie.plugins.manager import enable_plugins

def test_enable_plugins_none_returns_nullcontext():
    """When plugins_dir is None, enable_plugins should return a nullcontext."""
    ctx = enable_plugins(None)
    assert isinstance(ctx, type(nullcontext()))
    # Using the context manager should not raise any exception
    with ctx:
        pass

def test_enable_plugins_with_existing_directory():
    """When a valid directory is provided, enable_plugins should return a context manager
    that does not raise errors and is not a nullcontext."""
    tmp_dir = Path(__file__).parent / "tmp_plugins"
    tmp_dir.mkdir(exist_ok=True)
    # Create a dummy plugin file that would be ignored by the loader
    (tmp_dir / "dummy.py").write_text("# dummy plugin")
    ctx = enable_plugins(tmp_dir)
    assert not isinstance(ctx, type(nullcontext()))
    # Using the context manager should not raise any exception
    with ctx:
        pass

def test_enable_plugins_with_nonexistent_directory():
    """When a non-existent directory is provided, enable_plugins should still return a
    context manager that does not raise errors (the loader should handle missing paths)."""
    nonexistent = Path("/this/path/does/not/exist")
    ctx = enable_plugins(nonexistent)
    assert not isinstance(ctx, type(nullcontext()))
    with ctx:
        pass
