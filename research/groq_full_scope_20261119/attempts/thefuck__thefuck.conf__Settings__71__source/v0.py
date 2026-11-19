import os
import sys
import types
import importlib
import tempfile
import shutil
import pytest
from pathlib import Path

# Import the Settings class from the module under test
from thefuck.conf import Settings
from thefuck import const

@pytest.fixture
def settings_instance(tmp_path):
    """Create a Settings instance with a temporary user directory."""
    # Patch the environment to point to the temporary directory
    original_xdg = os.environ.get("XDG_CONFIG_HOME")
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    try:
        s = Settings()
        yield s
    finally:
        if original_xdg is not None:
            os.environ["XDG_CONFIG_HOME"] = original_xdg
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)

def test_init_creates_default_settings_file(settings_instance, tmp_path):
    """`init` should create a settings.py file with default headers and comments."""
    settings_instance.init()
    settings_file = tmp_path / "thefuck" / "settings.py"
    assert settings_file.is_file()
    content = settings_file.read_text()
    # Header must be present
    assert const.SETTINGS_HEADER.strip() in content
    # Each default setting should be commented
    for key, default in const.DEFAULT_SETTINGS.items():
        assert f"# {key} = {default}" in content

def test_env_overrides_settings(settings_instance, tmp_path):
    """Environment variables should override settings loaded from file."""
    # Write a custom value to the settings file
    settings_file = tmp_path / "thefuck" / "settings.py"
    settings_file.write_text("DEBUG = False\n")
    # Set environment variable to override
    os.environ["THEFUCK_DEBUG"] = "True"
    settings_instance.init()
    # The environment value should take precedence
    assert settings_instance["debug"] is True
    # Clean up
    os.environ.pop("THEFUCK_DEBUG")

def test_args_override_settings(settings_instance, tmp_path):
    """Command line arguments should override settings from file and env."""
    # Write a custom value to the settings file
    settings_file = tmp_path / "thefuck" / "settings.py"
    settings_file.write_text("REPEAT = 1\n")
    # Prepare a simple args namespace
    class Args:
        yes = False
        debug = False
        repeat = 5
    args = Args()
    settings_instance.init(args=args)
    # The args value should override the file value
    assert settings_instance["repeat"] == 5
