import logging
import sys
import io
import pytest
from tqdm.contrib.logging import tqdm_logging_redirect
from tqdm import trange

def test_logging_redirected_to_pbar_output(capsys):
    """When a log message is emitted inside the context, it appears in the tqdm bar output."""
    LOG = logging.getLogger("tqdm_test")
    LOG.setLevel(logging.INFO)

    # Capture stdout to inspect tqdm output
    with tqdm_logging_redirect(trange(3), total=3, leave=False) as pbar:
        LOG.info("Test message")
        # Advance the bar to force output
        for _ in range(3):
            pbar.update(1)

    # Capture the printed output
    captured = capsys.readouterr()
    # The log message should be present in the output (tqdm.write writes to stdout)
    assert "Test message" in captured.out
    # The progress bar should also be present
    assert "100%" in captured.out or "3/3" in captured.out

def test_zero_iterations_no_output(capsys):
    """If the iterable is empty, no progress bar or log output should appear."""
    LOG = logging.getLogger("tqdm_test_zero")
    LOG.setLevel(logging.INFO)

    with tqdm_logging_redirect(trange(0), total=0, leave=False) as pbar:
        LOG.info("Should not appear")
        # No updates

    captured = capsys.readouterr()
    # No progress bar or log message should be printed
    assert captured.out == ""

def test_default_loggers_use_root(capsys):
    """When no loggers are specified, the root logger is used for redirection."""
    LOG = logging.getLogger("tqdm_test_root")
    LOG.setLevel(logging.INFO)

    # Ensure root logger has a console handler
    root_handler = logging.StreamHandler(sys.stdout)
    logging.root.handlers = [root_handler]

    with tqdm_logging_redirect(trange(1), total=1, leave=False) as pbar:
        LOG.info("Root logger message")
        pbar.update(1)

    captured = capsys.readouterr()
    assert "Root logger message" in captured.out
    assert "100%" in captured.out or "1/1" in captured.out
