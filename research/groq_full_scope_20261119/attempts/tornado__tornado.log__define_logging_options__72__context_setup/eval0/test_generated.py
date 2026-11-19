import logging
import os
import tempfile
import shutil
import sys
import pytest
from tornado import options
from tornado.log import define_logging_options, enable_pretty_logging
from tornado.log import LogFormatter

# ---------------------------------------------------------------------------

def test_define_logging_options_adds_expected_flags(tmp_path):
    """define_logging_options should add all expected options to tornado.options."""
    # Create a fresh options instance
    opts = options.Options()
    define_logging_options(opts)
    # Check that each option is present with correct default
    assert opts.logging == "info"
    assert opts.log_to_stderr is None
    assert opts.log_file_prefix is None
    assert opts.log_file_max_size == 100 * 1000 * 1000
    assert opts.log_file_num_backups == 10
    assert opts.log_rotate_when == "midnight"
    assert opts.log_rotate_interval == 1
    assert opts.log_rotate_mode == "size"

def test_enable_pretty_logging_with_size_rotation(tmp_path):
    """enable_pretty_logging should create a RotatingFileHandler when log_file_prefix is set."""
    # Prepare a temporary log file prefix
    log_prefix = tmp_path / "test.log"
    # Configure options
    opts = options.Options()
    opts.define("logging", default="debug")
    opts.define("log_file_prefix", default=str(log_prefix))
    opts.define("log_file_max_size", default=1024)  # small size for quick rollover
    opts.define("log_file_num_backups", default=2)
    opts.define("log_rotate_mode", default="size")
    # Ensure no handlers yet
    root = logging.getLogger()
    root.handlers = []
    enable_pretty_logging(opts, root)
    # There should be two handlers: file and stderr
    handlers = root.handlers
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    # Emit a log message and verify file creation
    root.debug("test message")
    root.handlers[0].flush()
    assert log_prefix.exists()
    with open(log_prefix, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test message" in content

def test_enable_pretty_logging_invalid_rotate_mode_raises():
    """enable_pretty_logging should raise ValueError for unsupported rotate_mode."""
    opts = options.Options()
    opts.define("logging", default="info")
    opts.define("log_file_prefix", default="/dev/null")  # dummy
    opts.define("log_rotate_mode", default="invalid_mode")
    with pytest.raises(ValueError) as exc:
        enable_pretty_logging(opts)
    assert "The value of log_rotate_mode option should be" in str(exc.value)
