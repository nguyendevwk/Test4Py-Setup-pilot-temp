import io
import logging
import sys
import contextlib

import pytest
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import trange


def test_logging_redirected_to_tqdm_write(tmp_path):
    """When a console handler is present, messages are redirected to tqdm.write."""
    # Create a StringIO to capture tqdm.write output
    captured = io.StringIO()
    # Replace tqdm's default stream with our StringIO
    original_stdout = sys.stdout
    sys.stdout = captured
    try:
        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.INFO)
        # Ensure a console handler exists
        console_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(console_handler)

        with logging_redirect_tqdm([logger]):
            logger.info("Hello from logger")
            # Use tqdm to ensure progress bar is active
            for _ in trange(1, leave=False):
                pass

        # After exiting the context, the message should have been written via tqdm.write
        output = captured.getvalue()
        assert "Hello from logger" in output
        # tqdm.write prefixes the message with a newline if needed
        assert output.strip().endswith("Hello from logger")
    finally:
        sys.stdout = original_stdout


def test_original_handlers_restored_after_context():
    """After exiting the context, the original handlers are restored."""
    logger = logging.getLogger("restore_test")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)

    original_handlers = list(logger.handlers)

    with logging_redirect_tqdm([logger]):
        # Inside context, handlers should be replaced
        assert any(
            handler.__class__.__name__ == "_TqdmLoggingHandler"
            for handler in logger.handlers
        )

    # After context, handlers should match the original list
    assert logger.handlers == original_handlers


def test_no_console_handler_no_redirect(tmp_path):
    """If no console handler is found, no redirect occurs and logger remains unchanged."""
    logger = logging.getLogger("no_console")
    logger.setLevel(logging.INFO)
    # Add a file handler instead of console
    file_handler = logging.FileHandler(tmp_path / "log.txt")
    logger.addHandler(file_handler)

    original_handlers = list(logger.handlers)

    with logging_redirect_tqdm([logger]):
        # Inside context, handlers should remain unchanged
        assert logger.handlers == original_handlers

    # After context, handlers should still be unchanged
    assert logger.handlers == original_handlers
