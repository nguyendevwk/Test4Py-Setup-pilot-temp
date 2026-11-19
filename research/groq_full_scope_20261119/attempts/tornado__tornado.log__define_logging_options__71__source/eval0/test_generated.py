import importlib
import types
import tornado.log
import tornado.options
import pytest

def test_default_options_defined():
    # Ensure that calling define_logging_options with no argument
    # uses the global tornado.options.options and defines all flags.
    tornado.options.options.reset()
    tornado.log.define_logging_options()
    opts = tornado.options.options
    # Check that each expected flag is present with correct default
    assert opts.logging == "info"
    assert opts.log_to_stderr is None
    assert opts.log_file_prefix is None
    assert opts.log_file_max_size == 100 * 1000 * 1000
    assert opts.log_file_num_backups == 10
    assert opts.log_rotate_when == "midnight"
    assert opts.log_rotate_interval == 1
    assert opts.log_rotate_mode == "size"

def test_custom_options_defined(tmp_path):
    # Create a fresh Options instance and pass it to the function.
    custom_opts = tornado.options.Options()
    # Provide a log_file_prefix to test that string type is accepted.
    custom_opts.define("dummy", type=str, default="x")
    tornado.log.define_logging_options(custom_opts)
    # Verify that the custom option remains unchanged.
    assert custom_opts.dummy == "x"
    # Verify that logging options are added to the custom instance.
    assert custom_opts.logging == "info"
    assert custom_opts.log_file_prefix is None
    # Set a custom prefix and ensure it is stored.
    custom_opts.log_file_prefix = str(tmp_path / "log")
    assert custom_opts.log_file_prefix == str(tmp_path / "log")

def test_parse_callback_invoked(monkeypatch):
    # Patch enable_pretty_logging to track invocation.
    called = {"flag": False}
    def fake_enable_pretty_logging(opts):
        called["flag"] = True
    monkeypatch.setattr(tornado.log, "enable_pretty_logging", fake_enable_pretty_logging)

    # Use a fresh Options instance to avoid interference.
    opts = tornado.options.Options()
    tornado.log.define_logging_options(opts)
    # Trigger parsing to invoke the callback.
    opts.parse_args([])
    assert called["flag"], "enable_pretty_logging was not called during parse"
