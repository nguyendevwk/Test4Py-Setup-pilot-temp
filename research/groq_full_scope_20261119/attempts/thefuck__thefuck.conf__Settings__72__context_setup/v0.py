import os
import sys
import types
import importlib
import pytest
from pathlib import Path

# Import the Settings class from the real module
from thefuck.conf import Settings, const

# Helper to create a temporary user config directory
@pytest.fixture
def temp_user_dir(tmp_path):
    # Override XDG_CONFIG_HOME to point to tmp_path
    original = os.environ.get("XDG_CONFIG_HOME")
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    yield tmp_path
    if original is not None:
        os.environ["XDG_CONFIG_HOME"] = original
    else:
        del os.environ["XDG_CONFIG_HOME"]

# Test that Settings.init correctly loads defaults, file, env and args
def test_settings_init_loads_all_sources(temp_user_dir):
    # Create a minimal settings.py file with a custom value
    settings_file = temp_user_dir / "thefuck" / "settings.py"
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text("DEBUG = True\n")

    # Set environment variable to override a default
    os.environ["THEFUCK_DEBUG"] = "False"

    # Prepare argparse namespace with flags
    args = types.SimpleNamespace(yes=True, debug=False, repeat=3)

    # Instantiate Settings and initialize
    settings = Settings(const.DEFAULT_SETTINGS)
    settings.init(args=args)

    # Verify that the file value was loaded first
    assert settings["debug"] is True

    # Environment variable should override file value
    assert settings["debug"] is False

    # Args should override environment
    assert settings["debug"] is False  # args.debug is False, same as env
    assert settings["require_confirmation"] is False  # yes=True flips to False
    assert settings["repeat"] == 3

# Test that environment variables are parsed correctly for different types
def test_settings_env_parsing(temp_user_dir):
    # Set various environment variables
    os.environ["THEFUCK_RULES"] = "DEFAULT_RULES:my_rule"
    os.environ["THEFUCK_PRIORITY"] = "my_rule=5:other=10"
    os.environ["THEFUCK_WAIT_COMMAND"] = "2"
    os.environ["THEFUCK_REQUIRE_CONFIRMATION"] = "True"
    os.environ["THEFUCK_SLOW_COMMANDS"] = "cmd1:cmd2"

    settings = Settings(const.DEFAULT_SETTINGS)
    settings.init(args=None)

    # Rules should include default rules and the custom one
    assert "my_rule" in settings["rules"]
    assert "DEFAULT_RULES" in settings["rules"]

    # Priority should be a dict with correct integer values
    assert settings["priority"] == {"my_rule": 5, "other": 10}

    # Numeric and boolean conversions
    assert settings["wait_command"] == 2
    assert settings["require_confirmation"] is True

    # List conversion
    assert settings["slow_commands"] == ["cmd1", "cmd2"]

# Test that Settings._init_settings_file creates a file with default comments
def test_settings_file_creation(temp_user_dir):
    # Ensure the user directory does not exist yet
    user_dir = temp_user_dir / "thefuck"
    if user_dir.exists():
        for child in user_dir.iterdir():
            child.unlink()
        user_dir.rmdir()

    settings = Settings(const.DEFAULT_SETTINGS)
    settings.init(args=None)

    settings_file = user_dir / "settings.py"
    assert settings_file.is_file()

    # The file should start with the header and contain commented defaults
    content = settings_file.read_text()
    assert content.startswith(const.SETTINGS_HEADER)
    for key, default in const.DEFAULT_SETTINGS.items():
        assert f"# {key} = {default}" in content
