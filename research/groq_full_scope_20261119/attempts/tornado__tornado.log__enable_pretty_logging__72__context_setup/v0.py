import logging
import os
import sys
import tempfile
import types
import pytest
from tornado.log import enable_pretty_logging
from tornado.util import unicode_type

# Helper to create a simple options-like object
class DummyOptions:
    def __init__(
        self,
        logging="info",
        log_file_prefix=None,
        log_rotate_mode="size",
        log_file_max_size=1024,
        log_file_num_backups=1,
        log_rotate_when="D",
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

# Test 1: Normal configuration with file and stderr handlers
def test_enable_pretty_logging_file_and_stderr(tmp_path):
    log_file = tmp_path / "test.log"
    opts = DummyOptions(
        logging="debug",
        log_file_prefix=str(log_file),
        log_rotate_mode="size",
        log_file_max_size=10,
        log_file_num_backups=2,
        log_to_stderr=True,
    )
    logger = logging.getLogger("tornado_test")
    logger.handlers = []  # clear any existing handlers
    enable_pretty_logging(opts, logger)

    # Verify level
    assert logger.level == logging.DEBUG

    # Verify file handler exists and writes to file
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
    assert len(file_handlers) == 1
    fh = file_handlers[0]
    assert fh.baseFilename == str(log_file)
    assert fh.maxBytes == 10
    assert fh.backupCount == 2

    # Emit a log message and check file content
    logger.debug("test message")
    # Allow handler to flush
    for h in logger.handlers:
        h.flush()
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test message" in content

    # Verify stream handler exists
    stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(stream_handlers) == 1
    # Capture stdout to verify message appears
    captured = []
    original_stdout = sys.stdout
    try:
        sys.stdout = types.SimpleNamespace(write=captured.append)
        logger.info("stream test")
    finally:
        sys.stdout = original_stdout
    # The captured list contains the formatted log line
    assert any("stream test" in part for part in captured)

# Test 2: Invalid rotate mode raises ValueError
def test_enable_pretty_logging_invalid_rotate_mode():
    opts = DummyOptions(
        logging="info",
        log_file_prefix="dummy.log",
        log_rotate_mode="invalid_mode",
    )
    logger = logging.getLogger("tornado_test_invalid")
    logger.handlers = []
    with pytest.raises(ValueError) as excinfo:
        enable_pretty_logging(opts, logger)
    assert "The value of log_rotate_mode option should be" in str(excinfo.value)

# Test 3: Logging set to None or 'none' results in no changes
def test_enable_pretty_logging_no_logging(tmp_path):
    opts_none = DummyOptions(logging=None, log_to_stderr=False)
    opts_none_none = DummyOptions(logging="none", log_to_stderr=False)
    logger = logging.getLogger("tornado_test_none")
    logger.handlers = []
    # Capture original level and handlers
    original_level = logger.level
    original_handlers = list(logger.handlers)

    enable_pretty_logging(opts_none, logger)
    assert logger.level == original_level
    assert logger.handlers == original_handlers

    enable_pretty_logging(opts_none_none, logger)
    assert logger.level == original_level
    assert logger.handlers == original_handlers
