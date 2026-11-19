import logging
import sys
import io
import pytest
from tqdm.contrib.logging import tqdm_logging_redirect, logging_redirect_tqdm
from tqdm import tqdm


def test_tqdm_logging_redirect_basic(capsys):
    """Verify that logging messages are redirected to tqdm.write during a progress bar."""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    # Capture the output of tqdm.write by redirecting sys.stdout temporarily
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    with tqdm_logging_redirect(tqdm_class=tqdm, total=3) as pbar:
        for i in range(3):
            pbar.update()
            if i == 1:
                logger.info("test message")

    # Restore stdout
    output = sys.stdout.getvalue()
    sys.stdout = original_stdout

    # The output should contain the tqdm progress bar and the redirected log message
    assert "test message" in output
    assert "100%" in output or "3/3" in output


def test_tqdm_logging_redirect_zero_iterations(capsys):
    """Progress bar with zero total should not raise and still redirect logs."""
    logger = logging.getLogger("zero_logger")
    logger.setLevel(logging.INFO)

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    with tqdm_logging_redirect(tqdm_class=tqdm, total=0) as pbar:
        # No iterations, but log a message
        logger.info("zero iteration message")

    output = sys.stdout.getvalue()
    sys.stdout = original_stdout

    assert "zero iteration message" in output
    # The progress bar should indicate completion immediately
    assert "100%" in output or "0/0" in output


def test_tqdm_logging_redirect_invalid_tqdm_class():
    """Passing an invalid tqdm_class should raise a TypeError."""
    logger = logging.getLogger("invalid_logger")
    logger.setLevel(logging.INFO)

    with pytest.raises(TypeError):
        with tqdm_logging_redirect(tqdm_class="not_a_tqdm", total=1) as pbar:
            pbar.update()
            logger.info("should not reach here")
