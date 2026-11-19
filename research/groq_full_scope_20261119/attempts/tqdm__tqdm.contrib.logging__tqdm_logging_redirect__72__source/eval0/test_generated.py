import logging
import sys
import pytest
from tqdm.contrib.logging import tqdm_logging_redirect
from tqdm import tqdm as std_tqdm


def test_tqdm_logging_redirect_basic(capfd):
    """Verify that log messages are redirected to the tqdm progress bar."""
    logger = logging.getLogger("tqdm_test")
    logger.setLevel(logging.INFO)
    # Ensure logger has no handlers to avoid duplicate output
    logger.handlers = []

    with tqdm_logging_redirect(total=3, desc="test") as pbar:
        for i in range(3):
            logger.info(f"step {i}")
            pbar.update(1)

    out, err = capfd.readouterr()
    # The output should contain the tqdm bar and the log messages
    assert "test" in out
    assert "step 0" in out
    assert "step 1" in out
    assert "step 2" in out
    # The bar should reach 100% at the end
    assert "100%" in out or "100%" in out.splitlines()[-1]


def test_tqdm_logging_redirect_no_loggers(capfd):
    """When no loggers are provided, tqdm_logging_redirect should still work."""
    with tqdm_logging_redirect(total=2, desc="no_loggers") as pbar:
        for i in range(2):
            # Emit a log to the root logger; it should be ignored but not crash
            logging.getLogger().info(f"root log {i}")
            pbar.update(1)

    out, err = capfd.readouterr()
    assert "no_loggers" in out
    assert "100%" in out or "100%" in out.splitlines()[-1]


def test_tqdm_logging_redirect_invalid_tqdm_class():
    """Passing an invalid tqdm_class should raise a TypeError."""
    class BadTqdm:
        def __init__(self, *_, **__):
            raise TypeError("BadTqdm cannot be instantiated")

    with pytest.raises(TypeError, match="BadTqdm cannot be instantiated"):
        with tqdm_logging_redirect(total=1, tqdm_class=BadTqdm):
            pass
