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

def test_enable_pretty_logging_stream_and_level(tmp_path):
    # Configure options to log to stderr with level INFO
    opts = make_options(
        logging="info",
        log_file_prefix=None,
        log_file_rotate_mode=None,
        log_file_max_size=None,
        log_file_num_backups=None,
        log_file_rotate_when=None,
        log_file_rotate_interval=None,
        log_to_stderr=True,
    )
    logger = logging.getLogger("test_stream")
    logger.handlers = []  # clear any existing handlers
    enable_pretty_logging(opts, logger)

    # Assert level set to INFO
    assert logger.level == logging.INFO

    # Assert a StreamHandler was added
    stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(stream_handlers) == 1
    handler = stream_handlers[0]
    # Formatter should be LogFormatter with color enabled
    assert isinstance(handler.formatter, LogFormatter)
    assert handler.formatter.color is True

    # Emit a log and capture output
    stream = tempfile.TemporaryFile(mode="w+")
    handler.stream = stream
    logger.info("test message")
    stream.seek(0)
    output = stream.read()
    assert "test message" in output

def test_enable_pretty_logging_file_rotate_size(tmp_path):
    # Prepare a temporary file prefix
    prefix = tmp_path / "logfile.log"
    opts = make_options(
        logging="debug",
        log_file_prefix=str(prefix),
        log_file_rotate_mode="size",
        log_file_max_size=10,  # very small to trigger rotation
        log_file_num_backups=1,
        log_file_rotate_when=None,
        log_file_rotate_interval=None,
        log_to_stderr=False,
    )
    logger = logging.getLogger("test_file")
    logger.handlers = []
    enable_pretty_logging(opts, logger)

    # Assert a RotatingFileHandler was added
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
    assert len(file_handlers) == 1
    handler = file_handlers[0]
    assert handler.maxBytes == 10
    assert handler.backupCount == 1
    assert handler.baseFilename == str(prefix)

    # Emit many logs to trigger rotation
    for i in range(20):
        logger.debug(f"msg {i}")
    # After rotation, original file should exist and backup should exist
    assert prefix.exists()
    backup = prefix.with_name(prefix.name + ".1")
    assert backup.exists()

def test_enable_pretty_logging_invalid_rotate_mode_raises():
    opts = make_options(
        logging="warning",
        log_file_prefix="dummy.log",
        log_file_rotate_mode="invalid_mode",
        log_file_max_size=100,
        log_file_num_backups=2,
        log_file_rotate_when=None,
        log_file_rotate_interval=None,
        log_to_stderr=False,
    )
    logger = logging.getLogger("test_invalid")
    logger.handlers = []
    with pytest.raises(ValueError) as exc:
        enable_pretty_logging(opts, logger)
    assert "The value of log_rotate_mode option should be" in str(exc.value)
