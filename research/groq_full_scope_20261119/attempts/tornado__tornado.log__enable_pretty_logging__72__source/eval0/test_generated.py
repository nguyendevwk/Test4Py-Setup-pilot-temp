import logging
import os
import sys
import tempfile
import pytest
from tornado.log import enable_pretty_logging
from tornado.options import options as tornado_options

# Helper to reset tornado options between tests
def reset_tornado_options():
    tornado_options.logging = None
    tornado_options.log_file_prefix = None
    tornado_options.log_rotate_mode = None
    tornado_options.log_file_max_size = None
    tornado_options.log_file_num_backups = None
    tornado_options.log_rotate_when = None
    tornado_options.log_rotate_interval = None
    tornado_options.log_to_stderr = None

@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Remove any handlers added to root logger
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    reset_tornado_options()

def test_enable_pretty_logging_file_and_stderr(tmp_path):
    # Configure options to write to a file and stderr
    tornado_options.logging = "debug"
    tornado_options.log_file_prefix = str(tmp_path / "logfile.log")
    tornado_options.log_rotate_mode = "size"
    tornado_options.log_file_max_size = 1024
    tornado_options.log_file_num_backups = 1
    tornado_options.log_to_stderr = True

    enable_pretty_logging()

    root = logging.getLogger()
    # Check level
    assert root.level == logging.DEBUG

    # Verify file handler exists
    file_handler = next(
        (h for h in root.handlers if isinstance(h, logging.handlers.RotatingFileHandler)),
        None,
    )
    assert file_handler is not None
    assert file_handler.baseFilename == os.path.abspath(tornado_options.log_file_prefix)

    # Verify stream handler exists
    stream_handler = next(
        (h for h in root.handlers if isinstance(h, logging.StreamHandler)), None
    )
    assert stream_handler is not None
    # Emit a log and ensure file contains it
    root.debug("test message")
    with open(tornado_options.log_file_prefix, encoding="utf-8") as f:
        content = f.read()
    assert "test message" in content

def test_enable_pretty_logging_invalid_rotate_mode():
    tornado_options.logging = "info"
    tornado_options.log_file_prefix = "dummy.log"
    tornado_options.log_rotate_mode = "invalid_mode"

    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging()
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)

def test_enable_pretty_logging_no_logging_option():
    tornado_options.logging = None
    # Ensure no handlers are added when logging is None
    enable_pretty_logging()
    root = logging.getLogger()
    assert len(root.handlers) == 0
