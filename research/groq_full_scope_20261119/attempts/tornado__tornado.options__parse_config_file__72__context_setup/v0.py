import pytest
from pathlib import Path
from tornado.options import parse_config_file, options

def test_parse_config_file_sets_option_value(tmp_path: Path):
    # Define an option that will be set by the config file
    options.define("my_int", default=0, type=int, help="An integer option")
    # Create a config file that sets this option
    config = tmp_path / "config.cfg"
    config.write_text("my_int = 42\n")
    # Parse the config file
    parse_config_file(str(config))
    # Verify that the option value has been updated
    assert options.get("my_int") == 42

def test_parse_config_file_with_empty_file(tmp_path: Path):
    # Define an option with a default value
    options.define("empty_opt", default="default", type=str, help="Option for empty file test")
    # Create an empty config file
    empty_config = tmp_path / "empty.cfg"
    empty_config.write_text("")
    # Parsing an empty file should not raise an exception
    parse_config_file(str(empty_config))
    # The option should retain its default value
    assert options.get("empty_opt") == "default"

def test_parse_config_file_with_invalid_option_raises(tmp_path: Path):
    # Create a config file containing an unknown option
    bad_config = tmp_path / "bad.cfg"
    bad_config.write_text("unknown_option = 123\n")
    # Parsing should raise a ValueError indicating the unknown option
    with pytest.raises(ValueError) as excinfo:
        parse_config_file(str(bad_config))
    assert "unknown option" in str(excinfo.value).lower()
