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
        yield Settings()
    finally:
        if original_xdg is not None:
            os.environ["XDG_CONFIG_HOME"] = original_xdg
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)

def test_settings_file_creation_and_loading(settings_instance):
    """Verify that a default settings file is created and loaded correctly."""
    # The init method should create the settings file and load defaults
    settings_instance.init()
    # The settings file should exist
    settings_path = settings_instance.user_dir.joinpath("settings.py")
    assert settings_path.is_file()
    # The file should contain the header
    content = settings_path.read_text()
    assert const.SETTINGS_HEADER.strip() in content
    # The loaded settings should contain all default keys
    for key in const.DEFAULT_SETTINGS:
        assert key in settings_instance
        # The value should match the default unless overridden in the file
        if not content.splitlines()[0].startswith("#"):
            assert settings_instance[key] == const.DEFAULT_SETTINGS[key]

def test_settings_env_overrides(settings_instance):
    """Verify that environment variables override file and default settings."""
    # Set environment variables for a few settings
    os.environ["THEFUCK_RULES"] = "DEFAULT_RULES:my_rule"
    os.environ["THEFUCK_PRIORITY"] = "my_rule=5:other_rule=10"
    os.environ["THEFUCK_DEBUG"] = "True"
    os.environ["THEFUCK_HISTORY_LIMIT"] = "200"
    # Initialize settings
    settings_instance.init()
    # Check that the overrides took effect
    assert settings_instance.rules == ["my_rule"]
    assert settings_instance.priority == {"my_rule": 5, "other_rule": 10}
    assert settings_instance.debug is True
    assert settings_instance.history_limit == 200

def test_settings_args_override(settings_instance):
    """Verify that command‑line arguments override env and file settings."""
    # Prepare a fake args namespace
    class Args:
        yes = True
        debug = False
        repeat = 3
    args = Args()
    # Set an env variable that would normally override debug
    os.environ["THEFUCK_DEBUG"] = "True"
    # Initialize settings with args
    settings_instance.init(args=args)
    # The args should override env and defaults
    assert settings_instance.require_confirmation is False  # yes=True flips to False
    assert settings_instance.debug is False  # args.debug overrides env
    assert settings_instance.repeat == 3
