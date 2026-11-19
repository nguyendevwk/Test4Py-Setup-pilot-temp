import logging
import sys
import pytest
from tornado.log import define_logging_options
from tornado.options import Options, options as global_options


def test_define_logging_options_with_custom_instance(tmp_path):
    """Calling define_logging_options with a fresh Options instance
    should add all expected options with the correct defaults."""
    opts = Options()
    define_logging_options(opts)

    # Check that each option is defined and has the expected default value
    assert opts.logging == "info"
    assert opts.log_to_stderr is None
    assert opts.log_file_prefix is None
    assert opts.log_file_max_size == 100 * 1000 * 1000
    assert opts.log_file_num_backups == 10
    assert opts.log_rotate_when == "midnight"
    assert opts.log_rotate_interval == 1
    assert opts.log_rotate_mode == "size"

    # Ensure the option types are correct
    assert isinstance(opts.logging, str)
    assert isinstance(opts.log_to_stderr, (bool, type(None)))
    assert isinstance(opts.log_file_prefix, (str, type(None)))
    assert isinstance(opts.log_file_max_size, int)
    assert isinstance(opts.log_file_num_backups, int)
    assert isinstance(opts.log_rotate_when, str)
    assert isinstance(opts.log_rotate_interval, int)
    assert isinstance(opts.log_rotate_mode, str)


def test_define_logging_options_with_none_uses_global_options(tmp_path):
    """When None is passed, the global options instance should be used."""
    # Reset global options to a clean state
    global_options._definitions.clear()
    global_options._values.clear()

    define_logging_options(None)

    # Global options should now contain the logging options
    assert global_options.logging == "info"
    assert global_options.log_to_stderr is None
    assert global_options.log_file_prefix is None
    assert global_options.log_file_max_size == 100 * 1000 * 1000
    assert global_options.log_file_num_backups == 10
    assert global_options.log_rotate_when == "midnight"
    assert global_options.log_rotate_interval == 1
    assert global_options.log_rotate_mode == "size"


def test_define_logging_options_overrides_existing_values(tmp_path):
    """Options defined earlier should be overridden by define_logging_options."""
    opts = Options()
    # Predefine some options with different values
    opts.define("logging", default="warning")
    opts.define("log_file_max_size", default=50 * 1000 * 1000)

    # Now call define_logging_options to override them
    define_logging_options(opts)

    # The values should now match the defaults from define_logging_options
    assert opts.logging == "info"
    assert opts.log_file_max_size == 100 * 1000 * 1000
