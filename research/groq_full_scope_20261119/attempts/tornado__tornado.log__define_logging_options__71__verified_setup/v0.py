import logging
import pytest
from tornado.log import define_logging_options
from tornado.options import Options, options as global_options


def test_define_logging_options_default_global():
    """Calling with no argument should use the global options instance."""
    # Ensure the global options are clean
    global_options.reset()
    define_logging_options()
    # The global options should now contain the logging options
    assert hasattr(global_options, "logging")
    assert global_options.logging == "info"
    assert hasattr(global_options, "log_to_stderr")
    assert global_options.log_to_stderr is None
    assert hasattr(global_options, "log_file_prefix")
    assert global_options.log_file_prefix is None
    # Check a numeric default
    assert global_options.log_file_max_size == 100 * 1000 * 1000
    # Ensure the parse callback is registered
    callbacks = [cb for cb in global_options._parse_callbacks if cb.__name__ == "<lambda>"]
    assert callbacks, "Parse callback not registered"


def test_define_logging_options_custom_options():
    """Passing a custom Options instance should define the same set of options."""
    custom_opts = Options()
    define_logging_options(custom_opts)
    # Verify each option is present with expected defaults
    assert custom_opts.logging == "info"
    assert custom_opts.log_to_stderr is None
    assert custom_opts.log_file_prefix is None
    assert custom_opts.log_file_max_size == 100 * 1000 * 1000
    assert custom_opts.log_file_num_backups == 10
    assert custom_opts.log_rotate_when == "midnight"
    assert custom_opts.log_rotate_interval == 1
    assert custom_opts.log_rotate_mode == "size"
    # Ensure the parse callback is attached to the custom instance
    callbacks = [cb for cb in custom_opts._parse_callbacks if cb.__name__ == "<lambda>"]
    assert callbacks, "Parse callback not registered on custom options"


def test_define_logging_options_invalid_type():
    """Passing an object that lacks the 'define' method should raise AttributeError."""
    class BadOptions:
        pass

    bad_opts = BadOptions()
    with pytest.raises(AttributeError):
        define_logging_options(bad_opts)
