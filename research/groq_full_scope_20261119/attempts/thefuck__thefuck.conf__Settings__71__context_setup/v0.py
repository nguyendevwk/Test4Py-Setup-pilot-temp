import os
import sys
import builtins
import importlib
import types
import warnings
import pytest
from pathlib import Path

# Import the Settings class from the module under test
from thefuck.conf import Settings, const

# Helper to create a temporary user config directory
def create_user_dir(tmp_path):
    user_dir = tmp_path / "thefuck"
    user_dir.mkdir()
    return user_dir

@pytest.fixture
def settings_instance(tmp_path):
    # Patch the environment to use the temporary config directory
    original_xdg = os.environ.get("XDG_CONFIG_HOME")
    os.environ["XDG_CONFIG_HOME"] = str(tmp_path)
    try:
        settings = Settings(const.DEFAULT_SETTINGS)
        yield settings
    finally:
        if original_xdg is not None:
            os.environ["XDG_CONFIG_HOME"] = original_xdg
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)

def test_init_creates_settings_file_and_loads_defaults(settings_instance, tmp_path):
    """Test that init creates a settings.py file and loads default values."""
    # Ensure no settings file exists initially
    settings_file = tmp_path / "thefuck" / "settings.py"
    assert not settings_file.is_file()

    # Run init
    settings_instance.init()

    # After init, settings file should exist
    assert settings_file.is_file()
    # The file should contain the header and commented defaults
    content = settings_file.read_text()
    assert const.SETTINGS_HEADER.strip() in content
    for key, value in const.DEFAULT_SETTINGS.items():
        assert f"# {key} = {value}" in content

    # The settings dict should contain all default keys
    for key in const.DEFAULT_SETTINGS:
        assert key in settings_instance
        # Default values are loaded from the file (commented out), so they remain defaults
        assert settings_instance[key] == const.DEFAULT_SETTINGS[key]

def test_env_overrides_and_parsing(settings_instance, tmp_path):
    """Test that environment variables override defaults and are parsed correctly."""
    # Set environment variables to override some settings
    os.environ["THEFUCK_DEBUG"] = "True"
    os.environ["THEFUCK_REQUIRE_CONFIRMATION"] = "false"
    os.environ["THEFUCK_PRIORITY"] = "rule1=10:rule2=5"
    os.environ["THEFUCK_RULES"] = "DEFAULT_RULES:custom_rule"
    os.environ["THEFUCK_EXCLUDED_SEARCH_PATH_PREFIXES"] = "/tmp:/var"

    # Run init to load env
    settings_instance.init()

    # Check boolean parsing
    assert settings_instance["debug"] is True
    assert settings_instance["require_confirmation"] is False

    # Check priority parsing
    assert settings_instance["priority"] == {"rule1": 10, "rule2": 5}

    # Check rules parsing (DEFAULT_RULES should be expanded)
    expected_rules = const.DEFAULT_RULES + ["custom_rule"]
    assert settings_instance["rules"] == expected_rules

    # Check list parsing
    assert settings_instance["excluded_search_path_prefixes"] == ["/tmp", "/var"]

    # Clean up environment variables
    for var in ["THEFUCK_DEBUG", "THEFUCK_REQUIRE_CONFIRMATION",
                "THEFUCK_PRIORITY", "THEFUCK_RULES",
                "THEFUCK_EXCLUDED_SEARCH_PATH_PREFIXES"]:
        os.environ.pop(var, None)

def test_invalid_priority_string_is_skipped(settings_instance, tmp_path):
    """Test that malformed priority entries are ignored without raising."""
    # Set an invalid priority string
    os.environ["THEFUCK_PRIORITY"] = "rule1=abc:invalid_entry:rule2=20"

    # Capture warnings to ensure no exception is raised
    with warnings.catch_warnings(record=True) as w:
        settings_instance.init()

    # The priority dict should contain only the valid entry
    assert settings_instance["priority"] == {"rule2": 20}

    # No exception should have been raised, and no warning about the error
    assert not any("invalid" in str(record.message).lower() for record in w)

    # Clean up
    os.environ.pop("THEFUCK_PRIORITY", None)
