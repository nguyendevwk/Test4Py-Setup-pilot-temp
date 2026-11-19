import os
import pytest
from tornado.options import options, define, parse_config_file

# Ensure a clean state before each test
@pytest.fixture(autouse=True)
def reset_options():
    options._options = {}
    options._final = False
    yield
    options._options = {}
    options._final = False

def test_parse_config_file_sets_option(tmp_path):
    """Normal behavior: option value is updated from config file."""
    # Define an option with a default value
    define("foo", default=0, type=int, help="Test option")
    # Create a config file that sets foo to 42
    cfg_path = tmp_path / "config.cfg"
    cfg_path.write_text("foo=42\n")
    # Parse the config file
    parse_config_file(str(cfg_path))
    # Assert that the option value has been updated
    assert options.foo == 42

def test_parse_config_file_empty_file(tmp_path):
    """Boundary case: empty config file does not alter defaults."""
    define("bar", default="baz", type=str, help="Another test option")
    cfg_path = tmp_path / "empty.cfg"
    cfg_path.write_text("")  # empty file
    parse_config_file(str(cfg_path))
    # The default value should remain unchanged
    assert options.bar == "baz"

def test_parse_config_file_invalid_syntax(tmp_path):
    """Error case: malformed config file raises ValueError."""
    define("spam", default=True, type=bool, help="Bool option")
    cfg_path = tmp_path / "bad.cfg"
    # Write an invalid line that cannot be parsed
    cfg_path.write_text("spam = not_a_bool\n")
    with pytest.raises(ValueError):
        parse_config_file(str(cfg_path))
