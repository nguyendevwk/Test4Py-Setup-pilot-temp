import os
import pytest
from tornado import options
from tornado.options import define, options as tornado_options


def test_parse_config_file_sets_defined_option(tmp_path):
    # Define an option that will be set via the config file
    define("test_int", default=0, type=int, help="An integer option")
    # Create a config file that sets this option
    cfg_path = tmp_path / "config.cfg"
    cfg_path.write_text("test_int = 42\n")
    # Parse the config file
    options.parse_config_file(str(cfg_path))
    # Assert that the option value was updated
    assert tornado_options.test_int == 42


def test_parse_config_file_missing_file_raises(tmp_path):
    # Path to a non-existent file
    missing_path = tmp_path / "does_not_exist.cfg"
    # Parsing should raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        options.parse_config_file(str(missing_path))


def test_parse_config_file_empty_file_does_not_change_defaults(tmp_path):
    # Define an option with a known default
    define("test_str", default="default_value", type=str, help="A string option")
    # Create an empty config file
    empty_path = tmp_path / "empty.cfg"
    empty_path.write_text("")
    # Parse the empty file
    options.parse_config_file(str(empty_path))
    # The option should retain its default value
    assert tornado_options.test_str == "default_value"
