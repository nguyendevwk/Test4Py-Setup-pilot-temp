import builtins
import contextlib
import importlib
import types
import pytest
from pathlib import Path

# Import the target function and its module
from httpie.plugins.manager import enable_plugins, get_site_paths, _load_directories


def test_enable_plugins_none_returns_nullcontext():
    """
    When plugins_dir is None, enable_plugins should return a nullcontext
    that does nothing on enter/exit.
    """
    ctx = enable_plugins(None)
    assert isinstance(ctx, contextlib.nullcontext)
    # Entering and exiting should not raise
    with ctx:
        pass


def test_enable_plugins_calls_load_directories_with_site_paths(monkeypatch, tmp_path):
    """
    When a plugins_dir is provided, enable_plugins should call _load_directories
    with the result of get_site_paths(plugins_dir).
    """
    # Prepare a dummy site path list
    dummy_site_paths = [tmp_path / "site1", tmp_path / "site2"]

    # Patch get_site_paths to return our dummy list
    called = {}
    def fake_get_site_paths(path):
        called['path'] = path
        return dummy_site_paths
    monkeypatch.setattr(importlib.import_module('httpie.plugins.manager'), 'get_site_paths', fake_get_site_paths)

    # Patch _load_directories to capture its argument
    def fake_load_directories(paths):
        called['paths'] = paths
        return contextlib.nullcontext()
    monkeypatch.setattr(importlib.import_module('httpie.plugins.manager'), '_load_directories', fake_load_directories)

    # Call enable_plugins with a temporary directory
    ctx = enable_plugins(tmp_path)
    assert isinstance(ctx, contextlib.nullcontext)

    # Verify that get_site_paths was called with the correct argument
    assert called['path'] == tmp_path

    # Verify that _load_directories was called with the site paths returned by get_site_paths
    assert called['paths'] == dummy_site_paths


def test_enable_plugins_context_manager_behavior(monkeypatch, tmp_path):
    """
    Ensure that the context manager returned by enable_plugins properly
    enters and exits, and that the plugin loading side effects occur.
    """
    # Create a dummy plugin directory structure
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    # Create a dummy plugin file (empty)
    (plugin_dir / "dummy_plugin.py").write_text("# dummy plugin")

    # Patch get_site_paths to return the plugin directory
    monkeypatch.setattr(importlib.import_module('httpie.plugins.manager'), 'get_site_paths',
                       lambda path: [plugin_dir])

    # Patch _load_directories to return a context manager that records entry/exit
    entered = {'flag': False}
    def fake_load_directories(paths):
        assert paths == [plugin_dir]
        class DummyCtx:
            def __enter__(self):
                entered['flag'] = True
                return None
            def __exit__(self, exc_type, exc, tb):
                entered['flag'] = False
                return False
        return DummyCtx()
    monkeypatch.setattr(importlib.import_module('httpie.plugins.manager'), '_load_directories', fake_load_directories)

    ctx = enable_plugins(tmp_path)
    assert isinstance(ctx, types.SimpleNamespace) or isinstance(ctx, contextlib.AbstractContextManager)

    # Before entering, flag should be False
    assert not entered['flag']

    with ctx:
        # Inside context, flag should be True
        assert entered['flag']

    # After exiting, flag should be False again
    assert not entered['flag']
