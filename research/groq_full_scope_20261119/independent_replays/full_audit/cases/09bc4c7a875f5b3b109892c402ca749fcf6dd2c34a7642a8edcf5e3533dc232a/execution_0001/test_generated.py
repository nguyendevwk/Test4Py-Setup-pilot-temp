import logging
import os
import sys
import tempfile
import pytest
from tornado.log import enable_pretty_logging
from tornado.util import unicode_type, basestring_type

# Helper to create a simple options-like object
class DummyOptions:
    def __init__(
        self,
        logging="debug",
        log_file_prefix=None,
        log_rotate_mode="size",
        log_file_max_size=1024,
        log_file_num_backups=1,
        log_rotate_when="midnight",
        log_rotate_interval=1,
        log_to_stderr=True,
    ):
        self.logging = logging
        self.log_file_prefix = log_file_prefix
        self.log_rotate_mode = log_rotate_mode
        self.log_file_max_size = log_file_max_size
        self.log_file_num_backups = log_file_num_backups
        self.log_rotate_when = log_rotate_when
        self.log_rotate_interval = log_rotate_interval
        self.log_to_stderr = log_to_stderr

def test_enable_pretty_logging_with_file_and_stderr(tmp_path):
    """Normal case: file handler with size rotation and stderr handler."""
    log_file = tmp_path / "app.log"
    options = DummyOptions(
        logging="info",
        log_file_prefix=str(log_file),
        log_rotate_mode="size",
        log_file_max_size=10,  # small to trigger rotation quickly
        log_file_num_backups=2,
        log_to_stderr=True,
    )
    logger = logging.getLogger("test_logger")
    logger.handlers.clear()
    enable_pretty_logging(options, logger)

    # Verify level
    assert logger.level == logging.INFO

    # Verify handlers
    handlers = logger.handlers
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)

    # Emit a message and check file content
    logger.info("test message")
    # Allow handler to flush
    for h in handlers:
        h.flush()
    # File should exist and contain the message
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "test message" in content

def test_enable_pretty_logging_invalid_rotate_mode():
    """Error case: invalid rotate mode raises ValueError."""
    options = DummyOptions(
        logging="debug",
        log_file_prefix="dummy.log",
        log_rotate_mode="invalid_mode",
        log_to_stderr=False,
    )
    logger = logging.getLogger("test_logger_invalid")
    logger.handlers.clear()
    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging(options, logger)
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)

def test_enable_pretty_logging_no_logging():
    """Boundary case: options.logging is None or 'none' results in no changes."""
    options_none = DummyOptions(logging=None, log_to_stderr=False)
    options_none.logging = None
    logger = logging.getLogger("test_logger_none")
    logger.handlers.clear()
    enable_pretty_logging(options_none, logger)
    # No handlers should be added
    assert logger.handlers == []

    options_none.logging = "none"
    enable_pretty_logging(options_none, logger)
    assert logger.handlers == []
