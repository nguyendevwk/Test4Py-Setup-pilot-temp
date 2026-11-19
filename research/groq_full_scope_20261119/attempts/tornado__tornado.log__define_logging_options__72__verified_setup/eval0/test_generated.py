import logging
import pytest
from tornado.log import define_logging_options
from tornado.options import Options, options as global_options


def test_define_logging_options_with_custom_options(tmp_path):
    """When a custom Options instance is supplied, the logging options are added to it."""
    custom_opts = Options()
    define_logging_options(custom_opts)

    # All expected option names should be present
    expected_names = {
        "logging",
        "log_to_stderr",
        "log_file_prefix",
        "log_file_max_size",
        "log_file_num_backups",
        "log_rotate_when",
        "log_rotate_interval",
        "log_rotate_mode",
    }
    assert expected_names.issubset(set(custom_opts._options.keys()))

    # Verify that the default values are as documented
    assert custom_opts.logging == "info"
    assert custom_opts.log_to_stderr is None
    assert custom_opts.log_file_prefix is None
    assert custom_opts.log_file_max_size == 100 * 1000 * 1000
    assert custom_opts.log_file_num_backups == 10
    assert custom_opts.log_rotate_when == "midnight"
    assert custom_opts.log_rotate_interval == 1
    assert custom_opts.log_rotate_mode == "size"

    # Ensure that the callback is registered
    callbacks = [cb for cb in custom_opts._parse_callbacks]
    assert any(callable(cb) for cb in callbacks)


def test_define_logging_options_with_none(tmp_path):
    """When None is passed, the global options instance is used."""
    # Reset global options to a fresh instance for isolation
    global_options._options.clear()
    global_options._parse_callbacks.clear()

    define_logging_options(None)

    # The global options should now contain the logging options
    for name in (
        "logging",
        "log_to_stderr",
        "log_file_prefix",
        "log_file_max_size",
        "log_file_num_backups",
        "log_rotate_when",
        "log_rotate_interval",
        "log_rotate_mode",
    ):
        assert hasattr(global_options, name)

    # Check that the default values are correctly set
    assert global_options.logging == "info"
    assert global_options.log_file_max_size == 100 * 1000 * 1000
    assert global_options.log_rotate_mode == "size"


def test_define_logging_options_idempotent(tmp_path):
    """Calling define_logging_options twice should not overwrite existing definitions."""
    opts = Options()
    define_logging_options(opts)
    # Capture the initial values
    initial_logging = opts.logging
    initial_max_size = opts.log_file_max_size

    # Call again
    define_logging_options(opts)

    # Values should remain unchanged
    assert opts.logging == initial_logging
    assert opts.log_file_max_size == initial_max_size

    # No duplicate definitions should exist
    assert len(opts._options) == 8  # exactly the 8 options defined
