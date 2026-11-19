import logging
import os
import sys
import tempfile
import pytest
from tornado.log import enable_pretty_logging
from tornado.util import unicode_type, basestring_type

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

def test_enable_pretty_logging_file_and_stderr(tmp_path):
    """Verify that a rotating file handler and a stderr handler are added."""
    logger = logging.getLogger("test_logger_file_and_stderr")
    logger.handlers.clear()
    log_file = tmp_path / "log.txt"
    options = DummyOptions(
        logging="info",
        log_file_prefix=str(log_file),
        log_rotate_mode="size",
        log_file_max_size=10,
        log_file_num_backups=2,
        log_to_stderr=True,
    )
    enable_pretty_logging(options, logger)

    # Check level
    assert logger.level == logging.INFO

    # Handlers: one file, one stream
    handlers = logger.handlers
    assert len(handlers) == 2
    file_handler = next(h for h in handlers if isinstance(h, logging.handlers.RotatingFileHandler))
    stream_handler = next(h for h in handlers if isinstance(h, logging.StreamHandler))

    # File handler properties
    assert file_handler.baseFilename == str(log_file)
    assert file_handler.maxBytes == 10
    assert file_handler.backupCount == 2

    # Stream handler writes to stderr
    stream_handler.stream = sys.stderr
    logger.info("test message")
    # Ensure the file contains the message
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test message" in content

def test_enable_pretty_logging_invalid_rotate_mode():
    """Verify that an invalid rotate mode raises ValueError."""
    logger = logging.getLogger("test_logger_invalid_rotate")
    logger.handlers.clear()
    options = DummyOptions(
        logging="warning",
        log_file_prefix="dummy.log",
        log_rotate_mode="invalid_mode",
        log_to_stderr=False,
    )
    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging(options, logger)
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)

def test_enable_pretty_logging_no_logging_option():
    """Verify that no handlers are added when logging is None or 'none'."""
    logger = logging.getLogger("test_logger_no_logging")
    logger.handlers.clear()
    options_none = DummyOptions(logging=None, log_to_stderr=False)
    enable_pretty_logging(options_none, logger)
    assert logger.handlers == []

    options_none_str = DummyOptions(logging="none", log_to_stderr=False)
    enable_pretty_logging(options_none_str, logger)
    assert logger.handlers == []
