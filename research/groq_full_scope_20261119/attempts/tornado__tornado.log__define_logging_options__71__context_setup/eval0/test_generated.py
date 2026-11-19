import logging
import os
import tempfile
import shutil
import pytest
from tornado.log import define_logging_options, enable_pretty_logging
from tornado.options import Options

# Helper to create a fresh Options instance with no side effects
def fresh_options():
    return Options()

def test_size_rotation_handler(tmp_path):
    opts = fresh_options()
    define_logging_options(opts)
    # Configure options for size rotation
    opts.logging = "debug"
    opts.log_file_prefix = str(tmp_path / "logfile.log")
    opts.log_file_max_size = 1024  # small size for test
    opts.log_file_num_backups = 2
    opts.log_rotate_mode = "size"
    opts.log_to_stderr = False

    enable_pretty_logging(opts)
    logger = logging.getLogger()
    # Find the RotatingFileHandler
    file_handler = next(
        (h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)),
        None,
    )
    assert file_handler is not None, "RotatingFileHandler not added"
    assert file_handler.baseFilename == opts.log_file_prefix
    assert file_handler.maxBytes == opts.log_file_max_size
    assert file_handler.backupCount == opts.log_file_num_backups
    # Clean up handlers
    logger.handlers.clear()

def test_time_rotation_handler(tmp_path):
    opts = fresh_options()
    define_logging_options(opts)
    # Configure options for time rotation
    opts.logging = "info"
    opts.log_file_prefix = str(tmp_path / "time.log")
    opts.log_rotate_mode = "time"
    opts.log_rotate_when = "S"  # rotate every second
    opts.log_rotate_interval = 1
    opts.log_file_num_backups = 1
    opts.log_to_stderr = False

    enable_pretty_logging(opts)
    logger = logging.getLogger()
    # Find the TimedRotatingFileHandler
    time_handler = next(
        (h for h in logger.handlers if isinstance(h, logging.handlers.TimedRotatingFileHandler)),
        None,
    )
    assert time_handler is not None, "TimedRotatingFileHandler not added"
    assert time_handler.baseFilename == opts.log_file_prefix
    assert time_handler.when == opts.log_rotate_when
    assert time_handler.interval == opts.log_rotate_interval
    assert time_handler.backupCount == opts.log_file_num_backups
    # Clean up handlers
    logger.handlers.clear()

def test_invalid_rotate_mode_raises():
    opts = fresh_options()
    define_logging_options(opts)
    opts.logging = "warning"
    opts.log_file_prefix = "/dev/null"  # dummy path
    opts.log_rotate_mode = "invalid_mode"
    opts.log_to_stderr = False

    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging(opts)
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)
