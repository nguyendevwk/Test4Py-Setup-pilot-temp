import logging
import sys
import types
import pytest
from tqdm.contrib.logging import tqdm_logging_redirect
from tqdm.std import tqdm as std_tqdm


def test_tqdm_logging_redirect_yields_pbar(tmp_path):
    """The context manager yields a tqdm instance and updates the progress bar."""
    # Create a temporary file to write progress output
    out_file = tmp_path / "progress.txt"
    with tqdm_logging_redirect(total=5, file=out_file.open("w")) as pbar:
        # The yielded object should be a tqdm instance
        assert isinstance(pbar, std_tqdm)
        # Update the progress bar a few times
        for _ in range(3):
            pbar.update(1)
    # After exiting the context, the file should contain the final progress bar line
    out_file.seek(0)
    content = out_file.read()
    assert "100%" in content
    assert "5/5" in content


def test_tqdm_logging_redirect_accepts_loggers(tmp_path):
    """Passing a list of loggers does not raise an exception."""
    logger = logging.getLogger("tqdm_test")
    logger.setLevel(logging.INFO)
    # Ensure the logger has a handler so that messages are emitted
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # Use a dummy tqdm that writes to a file
    out_file = tmp_path / "log_progress.txt"
    with tqdm_logging_redirect(
        total=2,
        file=out_file.open("w"),
        loggers=[logger],
    ) as pbar:
        # Emit a log message that should be redirected to tqdm
        logger.info("Test message")
        pbar.update(1)
    # Verify that the log message appears in the progress output
    out_file.seek(0)
    content = out_file.read()
    assert "Test message" in content
    assert "50%" in content


def test_tqdm_logging_redirect_custom_tqdm_class(tmp_path):
    """A custom tqdm class is used when supplied via tqdm_class."""
    # Define a custom tqdm subclass that records the arguments it was instantiated with
    class RecordingTqdm(std_tqdm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.recorded_args = args
            self.recorded_kwargs = kwargs

    out_file = tmp_path / "custom_progress.txt"
    with tqdm_logging_redirect(
        total=1,
        file=out_file.open("w"),
        tqdm_class=RecordingTqdm,
    ) as pbar:
        assert isinstance(pbar, RecordingTqdm)
        # The custom class should have recorded the arguments
        assert pbar.recorded_args == ()
        assert pbar.recorded_kwargs["total"] == 1
        pbar.update(1)
    out_file.seek(0)
    content = out_file.read()
    assert "100%" in content
