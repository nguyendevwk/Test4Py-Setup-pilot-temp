import os
import pytest
from tornado import options
from tornado.options import define, options as tornado_options

# Ensure a clean state before each test
@pytest.fixture(autouse=True)
def reset_options():
    tornado_options._options = {}
    tornado_options._defined = {}
    tornado_options._final = False
    yield
    tornado_options._options = {}
    tornado_options._defined = {}
    tornado_options._final = False

def test_parse_config_file_sets_defined_options(tmp_path):
    # Define an option that will be set via config file
    define("test_int", default=0, type=int, help="An integer option")
    define("test_str", default="default", type=str, help="A string option")

    # Create a config file that sets these options
    config = tmp_path / "config.ini"
    config.write_text(
        """
        test_int = 42
        test_str = hello
        """
    )

    # Parse the config file
    options.parse_config_file(str(config), final=True)

    # Assert that the options have been updated
    assert tornado_options.test_int == 42
    assert tornado_options.test_str == "hello"

def test_parse_config_file_missing_file_raises(tmp_path):
    # Define an option to ensure options module is initialized
    define("dummy", default="x", type=str, help="dummy option")

    # Path to a non-existent file
    missing_path = tmp_path / "nonexistent.ini"

    # Parsing a missing file should raise IOError (or OSError)
    with pytest.raises((IOError, OSError)):
        options.parse_config_file(str(missing_path), final=False)

def test_parse_config_file_empty_file_does_not_change_defaults(tmp_path):
    # Define an option with a default value
    define("empty_test", default="unchanged", type=str, help="empty file test")

    # Create an empty config file
    empty_config = tmp_path / "empty.ini"
    empty_config.write_text("")

    # Parse the empty file
    options.parse_config_file(str(empty_config), final=False)

    # The option should retain its default value
    assert tornado_options.empty_test == "unchanged"
