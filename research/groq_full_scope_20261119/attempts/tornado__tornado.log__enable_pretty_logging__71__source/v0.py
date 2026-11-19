import logging
import os
import sys
import tempfile
import types
import pytest
from tornado.log import enable_pretty_logging
from tornado.log import LogFormatter

# Helper to create a minimal options object
def make_options(**kwargs):
    opts = types.SimpleNamespace()
    for k, v in kwargs.items():
        setattr(opts, k, v)
    return opts

def test_enable_pretty_logging_stderr_and_file(tmp_path):
    # Create a temporary file prefix
    log_file = tmp_path / "log.txt"
    # Options: log to stderr and to a file with size rotation
    opts = make_options(
        logging="debug",
        log_file_prefix=str(log_file),
        log_rotate_mode="size",
        log_file_max_size=1024,
        log_file_num_backups=1,
        log_to_stderr=True,
    )
    logger = logging.getLogger("test_logger")
    logger.handlers = []  # clear any existing handlers
    enable_pretty_logging(opts, logger)

    # Check that the logger level is set to DEBUG
    assert logger.level == logging.DEBUG

    # There should be two handlers: one StreamHandler and one RotatingFileHandler
    handlers = logger.handlers
    assert len(handlers) == 2
    stream_handler = next(h for h in handlers if isinstance(h, logging.StreamHandler))
    file_handler = next(h for h in handlers if isinstance(h, logging.handlers.RotatingFileHandler))

    # Verify stream handler uses LogFormatter with color
    assert isinstance(stream_handler.formatter, LogFormatter)
    assert stream_handler.formatter.color is True

    # Verify file handler uses LogFormatter without color
    assert isinstance(file_handler.formatter, LogFormatter)
    assert file_handler.formatter.color is False

    # Emit a log record and ensure it is written to both destinations
    logger.debug("test message")
    # Check stderr output
    # (We cannot capture stderr easily without redirecting, so skip that part)
    # Check file content
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test message" in content

def test_enable_pretty_logging_invalid_rotate_mode():
    # Options with an invalid rotate mode should raise ValueError
    opts = make_options(
        logging="info",
        log_file_prefix="dummy.log",
        log_rotate_mode="invalid_mode",
        log_file_max_size=1024,
        log_file_num_backups=1,
    )
    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging(opts)
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)

def test_enable_pretty_logging_no_logging_option():
    # When options.logging is None or "none", the function should return without adding handlers
    opts = make_options(
        logging=None,
        log_file_prefix="dummy.log",
        log_rotate_mode="size",
        log_file_max_size=1024,
        log_file_num_backups=1,
        log_to_stderr=True,
    )
    logger = logging.getLogger("test_logger_no_logging")
    logger.handlers = []
    enable_pretty_logging(opts, logger)
    # No handlers should be added
    assert logger.handlers == []
