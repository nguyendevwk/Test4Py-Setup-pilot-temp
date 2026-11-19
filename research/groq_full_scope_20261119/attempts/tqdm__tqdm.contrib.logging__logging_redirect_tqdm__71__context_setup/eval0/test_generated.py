import logging
import sys
import io
import contextlib

import pytest
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm


def test_logging_redirect_to_tqdm_write(tmp_path):
    """When a console logger is redirected, messages are written via tqdm.write."""
    # Prepare a logger that writes to a StringIO stream
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.INFO)
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    logger.handlers = [handler]

    # Capture stdout to verify tqdm.write output
    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        with logging_redirect_tqdm([logger]):
            logger.info("redirected message")

    # The message should appear in the captured stdout via tqdm.write
    output = stdout_capture.getvalue()
    assert "redirected message" in output
    # The original handler should not have written to its stream
    assert stream.getvalue() == ""


def test_original_handlers_restored_after_context():
    """After exiting the context, the original handlers are restored."""
    logger = logging.getLogger("restore_logger")
    logger.setLevel(logging.INFO)
    original_handler = logging.StreamHandler(sys.stderr)
    logger.handlers = [original_handler]

    # Capture stderr to ensure original handler writes after context
    stderr_capture = io.StringIO()
    with contextlib.redirect_stderr(stderr_capture):
        with logging_redirect_tqdm([logger]):
            logger.info("inside context")
        logger.info("outside context")

    # Inside context, message should not appear on stderr
    assert "inside context" not in stderr_capture.getvalue()
    # Outside context, original handler should write to stderr
    assert "outside context" in stderr_capture.getvalue()


def test_no_loggers_default_behavior(tmp_path):
    """When no loggers are provided, the root logger is used and restored."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    original_handlers = root_logger.handlers.copy()

    # Capture stdout to verify tqdm.write output
    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        with logging_redirect_tqdm():
            root_logger.info("root message")

    output = stdout_capture.getvalue()
    assert "root message" in output
    # After context, handlers should match the original ones
    assert root_logger.handlers == original_handlers
