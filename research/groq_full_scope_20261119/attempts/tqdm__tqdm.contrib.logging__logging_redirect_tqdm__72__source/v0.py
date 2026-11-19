import logging
import sys
import io
import contextlib
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm as std_tqdm

# Helper to capture tqdm.write output
class CaptureTqdm(std_tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured = []

    def write(self, msg, end="\n", file=None, **kwargs):
        self.captured.append(msg)
        super().write(msg, end=end, file=file, **kwargs)

def test_logging_redirect_to_tqdm_write(tmp_path):
    # Setup a logger with a console handler
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.handlers = [console_handler]

    # Capture stdout to verify that tqdm.write writes to it
    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        with logging_redirect_tqdm([logger]):
            logger.info("Test message")
    # After context, the message should have been written via tqdm.write
    output = stdout_capture.getvalue()
    assert "Test message" in output

    # Ensure console handler is removed and restored after context
    assert console_handler not in logger.handlers
    # After exiting, original handlers should be restored
    with logging_redirect_tqdm([logger]):
        pass
    assert console_handler in logger.handlers

def test_logging_redirect_with_file_handler(tmp_path):
    # Logger with both console and file handlers
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(tmp_path / "log.txt")
    console_handler = logging.StreamHandler(sys.stdout)
    logger.handlers = [file_handler, console_handler]

    # Capture stdout
    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        with logging_redirect_tqdm([logger]):
            logger.info("File and console message")
    # Message should appear in stdout via tqdm.write
    assert "File and console message" in stdout_capture.getvalue()
    # Message should also be written to the file
    with open(tmp_path / "log.txt", "r") as f:
        file_content = f.read()
    assert "File and console message" in file_content

def test_logging_redirect_with_custom_tqdm_class(tmp_path):
    # Logger with console handler
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    logger.handlers = [console_handler]

    # Use a custom tqdm class that records writes
    capture = CaptureTqdm()
    with logging_redirect_tqdm([logger], tqdm_class=lambda *a, **k: capture):
        logger.info("Custom tqdm message")
    # The custom tqdm instance should have captured the message
    assert "Custom tqdm message" in capture.captured
    # Ensure that the console handler is not present after context
    assert console_handler not in logger.handlers
