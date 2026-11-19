import logging
import sys
import io
import contextlib

import pytest

from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm


def _capture_output(func, *args, **kwargs):
    """Helper to capture stdout and stderr during func execution."""
    buf_out = io.StringIO()
    buf_err = io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        func(*args, **kwargs)
    return buf_out.getvalue(), buf_err.getvalue()


def test_logging_redirected_to_tqdm_write(tmp_path):
    """When inside the context, console logs are redirected to tqdm.write."""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    # Attach a console handler that writes to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers = [console_handler]

    # Capture output before context to ensure nothing is printed
    out_before, err_before = _capture_output(logger.info, "before")
    assert out_before == ""
    assert err_before == ""

    with logging_redirect_tqdm([logger]):
        # Inside context, the message should go to tqdm.write (stderr)
        out_inside, err_inside = _capture_output(logger.info, "inside")
        # tqdm.write writes to stderr by default
        assert "inside" in err_inside
        assert out_inside == ""

    # After context, original handler restored; message goes to stdout
    out_after, err_after = _capture_output(logger.info, "after")
    assert out_after.strip() == "after"
    assert err_after == ""


def test_default_loggers_use_logging_root(tmp_path):
    """When no loggers are provided, the root logger is used."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # Attach a console handler to root
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.handlers = [console_handler]

    out_before, err_before = _capture_output(root_logger.info, "root before")
    assert out_before == ""
    assert err_before == ""

    with logging_redirect_tqdm():
        out_inside, err_inside = _capture_output(root_logger.info, "root inside")
        assert "root inside" in err_inside
        assert out_inside == ""

    out_after, err_after = _capture_output(root_logger.info, "root after")
    assert out_after.strip() == "root after"
    assert err_after == ""


def test_multiple_loggers_and_restoration(tmp_path):
    """Multiple loggers are redirected and restored correctly."""
    logger_a = logging.getLogger("logger_a")
    logger_b = logging.getLogger("logger_b")
    for logger in (logger_a, logger_b):
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.handlers = [console_handler]

    # Capture before context
    out_a_before, err_a_before = _capture_output(logger_a.info, "a before")
    out_b_before, err_b_before = _capture_output(logger_b.info, "b before")
    assert out_a_before == "" and err_a_before == ""
    assert out_b_before == "" and err_b_before == ""

    with logging_redirect_tqdm([logger_a, logger_b]):
        out_a_inside, err_a_inside = _capture_output(logger_a.info, "a inside")
        out_b_inside, err_b_inside = _capture_output(logger_b.info, "b inside")
        # Both should be redirected to stderr via tqdm.write
        assert "a inside" in err_a_inside
        assert out_a_inside == ""
        assert "b inside" in err_b_inside
        assert out_b_inside == ""

    # After context, both should output to stdout
    out_a_after, err_a_after = _capture_output(logger_a.info, "a after")
    out_b_after, err_b_after = _capture_output(logger_b.info, "b after")
    assert out_a_after.strip() == "a after"
    assert err_a_after == ""
    assert out_b_after.strip() == "b after"
    assert err_b_after == ""
