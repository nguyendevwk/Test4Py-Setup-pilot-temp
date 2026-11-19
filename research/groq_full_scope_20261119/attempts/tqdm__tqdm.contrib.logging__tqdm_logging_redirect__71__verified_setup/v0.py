import logging
import sys
import io
import pytest
from tqdm.contrib.logging import tqdm_logging_redirect
from tqdm import tqdm as std_tqdm

def test_logging_redirect_to_tqdm_output(capsys):
    """Messages logged inside the context are written to the tqdm bar."""
    logger = logging.getLogger("tqdm_test")
    logger.setLevel(logging.INFO)
    # Ensure no handlers interfere
    logger.handlers = []

    with tqdm_logging_redirect(total=3, desc="test") as pbar:
        logger.info("Hello from tqdm")
        pbar.update(1)
        logger.info("Another message")
        pbar.update(1)
        logger.info("Final message")
        pbar.update(1)

    # Capture stdout and check that the logged messages appear
    captured = capsys.readouterr()
    # The messages should be present in the output, each on a new line
    assert "Hello from tqdm" in captured.out
    assert "Another message" in captured.out
    assert "Final message" in captured.out

def test_logging_redirect_with_custom_logger_and_stream(capsys):
    """Custom logger with a stream handler receives messages via tqdm."""
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)
    logger.handlers = [handler]

    with tqdm_logging_redirect(total=2, desc="custom", loggers=[logger]) as pbar:
        logger.debug("Debug message")
        pbar.update(1)
        logger.warning("Warning message")
        pbar.update(1)

    # The stream should contain the messages, not the stdout
    stream_contents = stream.getvalue()
    assert "Debug message" in stream_contents
    assert "Warning message" in stream_contents
    # The stdout should not contain the messages (only the tqdm bar)
    captured = capsys.readouterr()
    assert "Debug message" not in captured.out
    assert "Warning message" not in captured.out

def test_invalid_tqdm_class_raises_type_error():
    """Passing a non-callable as tqdm_class should raise a TypeError."""
    with pytest.raises(TypeError):
        with tqdm_logging_redirect(total=1, tqdm_class="not_a_class") as pbar:
            # The context manager should fail before yielding
            pass
