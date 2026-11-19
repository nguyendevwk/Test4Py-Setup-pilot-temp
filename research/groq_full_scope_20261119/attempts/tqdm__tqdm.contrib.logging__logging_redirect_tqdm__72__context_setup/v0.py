import logging
import sys
import io
import contextlib

import pytest

from tqdm.contrib.logging import logging_redirect_tqdm, _TqdmLoggingHandler


def test_logging_redirect_to_tqdm_write(tmp_path):
    """When a console handler is present, messages are written via tqdm.write."""
    # Create a logger with a console StreamHandler
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    stream = io.StringIO()
    console_handler = logging.StreamHandler(stream)
    logger.handlers = [console_handler]

    # Capture tqdm.write output
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        with logging_redirect_tqdm([logger]):
            logger.info("redirected message")

    # The message should appear in the captured stdout via tqdm.write
    output = captured.getvalue()
    assert "redirected message" in output
    # The original console handler should not output to its stream
    assert stream.getvalue() == ""


def test_no_console_handler_restores_original(tmp_path):
    """If a logger has no console handler, its handlers are unchanged after exit."""
    logger = logging.getLogger("no_console")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(tmp_path / "log.txt")
    logger.handlers = [file_handler]

    original_handlers = list(logger.handlers)

    with logging_redirect_tqdm([logger]):
        logger.info("message during context")

    # After exiting, handlers should be restored to original
    assert logger.handlers == original_handlers
    # The file should contain the message
    with open(tmp_path / "log.txt", "r") as f:
        content = f.read()
    assert "message during context" in content


def test_default_loggers_use_root_and_restore(tmp_path):
    """When no loggers are provided, the root logger is used and restored."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    stream = io.StringIO()
    console_handler = logging.StreamHandler(stream)
    root.handlers = [console_handler]

    with logging_redirect_tqdm():
        logging.info("root message")

    # After context, root handlers should be restored
    assert root.handlers == [console_handler]
    # The message should have been redirected via tqdm.write
    # Since tqdm.write writes to stdout, capture it
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        logging.info("root message")
    assert "root message" in captured.getvalue()
