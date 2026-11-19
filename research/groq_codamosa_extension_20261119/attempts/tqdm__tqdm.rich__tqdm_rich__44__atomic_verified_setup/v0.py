import pytest
from tqdm.rich import tqdm_rich
from tqdm.std import TqdmExperimentalWarning
import warnings
import io
import sys

def test_tqdm_rich_normal_iteration(capsys):
    """Verify that tqdm_rich iterates correctly and displays progress."""
    with tqdm_rich(total=3, leave=False, disable=False) as pbar:
        for _ in pbar:
            pass
    # Capture stdout to ensure the progress bar was printed
    captured = capsys.readouterr()
    # The final line should contain the completion percentage (100%)
    assert "100%" in captured.out
    # The description should be empty by default
    assert "[]" not in captured.out  # no description brackets

def test_tqdm_rich_disable_no_gui(capsys):
    """When disable=True, tqdm_rich should not initialize the rich GUI."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        with tqdm_rich(total=2, disable=True) as pbar:
            for _ in pbar:
                pass
    # No warnings should be emitted because GUI is disabled
    assert not any(item.category is TqdmExperimentalWarning for item in w)
    # Capture stdout to ensure nothing was printed
    captured = capsys.readouterr()
    assert captured.out == ""

def test_tqdm_rich_invalid_progress_type():
    """Passing a non-tuple progress argument should raise a TypeError."""
    with pytest.raises(TypeError):
        # progress expects a tuple; passing a string triggers a TypeError in Progress
        tqdm_rich(total=1, progress="invalid")
