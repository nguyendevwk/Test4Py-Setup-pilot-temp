import logging
import sys
import io
import contextlib
import pytest
from tqdm import trange
from tqdm.contrib.logging import logging_redirect_tqdm, _TqdmLoggingHandler, _get_first_found_console_logging_handler, _is_console_logging_handler

# Test 1: Basic redirection of root logger to tqdm.write
def test_logging_redirect_basic(capsys):
    LOG = logging.getLogger("test_basic")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    with logging_redirect_tqdm():
        for i in trange(5, desc="test"):
            if i == 2:
                LOG.info("redirected message")
    # Capture stdout after context
    out, err = capsys.readouterr()
    # The tqdm progress bar should be present
    assert "test" in out
    # The redirected log message should appear via tqdm.write (prefixed by a newline)
    assert "redirected message" in out
    # Ensure no duplicate handlers: only one INFO message
    assert out.count("redirected message") == 1

# Test 2: Redirection with a custom logger and file handler
def test_logging_redirect_custom_logger(tmp_path):
    LOG = logging.getLogger("test_custom")
    # Add a file handler that should remain unaffected
    file_path = tmp_path / "log.txt"
    file_handler = logging.FileHandler(file_path, mode="w")
    file_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    LOG.addHandler(file_handler)
    LOG.setLevel(logging.INFO)

    with logging_redirect_tqdm(loggers=[LOG]):
        LOG.info("inside context")
    # After context, file should contain the log
    with open(file_path, "r") as f:
        content = f.read()
    assert "INFO:inside context" in content
    # The console output should contain the message via tqdm.write
    # Capture stdout
    out, _ = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out):
        LOG.info("outside context")
    # Outside context, message goes to original handler (file only), so stdout should be empty
    assert out.getvalue() == ""

# Test 3: Ensure that non-console handlers are preserved and console handlers are replaced
def test_logging_redirect_preserve_non_console():
    LOG = logging.getLogger("test_preserve")
    # Add a console handler with a custom formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(">>> %(message)s"))
    LOG.addHandler(console_handler)
    LOG.setLevel(logging.INFO)

    # Capture stdout
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        with logging_redirect_tqdm(loggers=[LOG]):
            LOG.info("inside")
    # The message should be redirected via tqdm.write, not the original console handler
    # tqdm.write prefixes with a newline and does not use the formatter
    captured = out.getvalue()
    assert "inside" in captured
    assert ">>>" not in captured  # original formatter should not appear
    # After context, original console handler should be restored
    out2 = io.StringIO()
    with contextlib.redirect_stdout(out2):
        LOG.info("outside")
    assert ">>> outside" in out2.getvalue()
