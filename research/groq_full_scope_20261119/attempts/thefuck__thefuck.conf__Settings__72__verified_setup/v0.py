import os
import sys
import types
import importlib
import tempfile
import shutil
import pytest
from thefuck.conf import Settings
from thefuck import const

@pytest.fixture
def settings_instance(tmp_path):
    """Create a Settings instance with a temporary user directory."""
    # Patch the environment to point to the temporary config directory
    original_xdg = os.environ.get("XDG_CONFIG_HOME")
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    try:
        s = Settings()
        yield s
    finally:
        if original_xdg is None:
            del os.environ["XDG_CONFIG_HOME"]
        else:
            os.environ["XDG_CONFIG_HOME"] = original_xdg

def test_settings_file_creation_and_loading(settings_instance):
    """Verify that a default settings file is created and loaded correctly."""
    s = settings_instance
    # The init method should create the settings file and load defaults
    s.init()
    # The file should exist
    settings_path = s.user_dir.joinpath("settings.py")
    assert settings_path.is_file()
    # The loaded settings should contain all default keys
    for key in const.DEFAULT_SETTINGS:
        assert key in s
        # Default values should match the defaults unless overridden
        assert s[key] == const.DEFAULT_SETTINGS[key]
    # Modify the settings file to change a value
    with settings_path.open("a", encoding="utf-8") as f:
        f.write("\nSOME_NEW_SETTING = 42\n")
    # Reinitialize to load the new setting
    s.init()
    assert s.get("SOME_NEW_SETTING") == 42

def test_settings_env_overrides(settings_instance):
    """Verify that environment variables override file settings."""
    s = settings_instance
    # Create a settings file with a known value
    settings_path = s.user_dir.joinpath("settings.py")
    settings_path.write_text("DEBUG = False\n", encoding="utf-8")
    # Set environment variable to override DEBUG
    os.environ["THEFUCK_DEBUG"] = "True"
    s.init()
    # The environment value should override the file value
    assert s["debug"] is True
    # Clean up
    del os.environ["THEFUCK_DEBUG"]

def test_settings_args_overrides(settings_instance):
    """Verify that command line arguments override env and file settings."""
    s = settings_instance
    # Create a settings file with a known value
    settings_path = s.user_dir.joinpath("settings.py")
    settings_path.write_text("REPEAT = 1\n", encoding="utf-8")
    # Set environment variable to override REPEAT
    os.environ["THEFUCK_REPEAT"] = "2"
    # Prepare a simple args namespace
    class Args:
        yes = False
        debug = False
        repeat = 3
    args = Args()
    s.init(args=args)
    # The args value should override env and file
    assert s["repeat"] == 3
    # Clean up
    del os.environ["THEFUCK_REPEAT"]
