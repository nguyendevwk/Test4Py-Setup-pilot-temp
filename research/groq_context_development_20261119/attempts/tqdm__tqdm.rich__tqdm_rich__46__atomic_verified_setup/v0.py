import warnings
import pytest
from tqdm.rich import tqdm_rich
from tqdm import tqdm as std_tqdm


def test_tqdm_rich_normal_progress(tmp_path):
    """Verify that tqdm_rich updates progress and emits experimental warning."""
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Create a list to iterate over
        data = list(range(5))
        # Instantiate tqdm_rich with a custom description
        pbar = tqdm_rich(data, desc="test", leave=False, disable=False)
        # Iterate through the data
        for _ in pbar:
            pass
        # Close the progress bar
        pbar.close()

    # Check that the experimental warning was emitted
    assert any(
        issubclass(warning.category, std_tqdm.TqdmExperimentalWarning)
        for warning in w
    ), "Expected TqdmExperimentalWarning to be emitted"

    # After closing, the progress bar should be finished
    # The internal task should have completed all iterations
    assert pbar.n == len(data), "Progress bar did not complete all iterations"
    # The progress bar should have been marked as finished
    assert pbar._prog.finished, "Progress bar not marked as finished after close"


def test_tqdm_rich_disable_no_warning_and_no_progress(tmp_path):
    """Verify that disabling tqdm_rich suppresses warnings and progress updates."""
    # Capture warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        data = list(range(3))
        pbar = tqdm_rich(data, desc="disabled", disable=True)
        # Iterate through the data
        for _ in pbar:
            pass
        pbar.close()

    # No experimental warning should be emitted
    assert not any(
        issubclass(warning.category, std_tqdm.TqdmExperimentalWarning)
        for warning in w
    ), "Unexpected TqdmExperimentalWarning when disabled"

    # The progress bar should not have created a task
    assert not hasattr(pbar, "_task_id"), "Task should not be created when disabled"
    # The internal counter should still reflect iterations
    assert pbar.n == len(data), "Counter did not increment when disabled"


def test_tqdm_rich_generator_total_none(tmp_path):
    """Verify that tqdm_rich handles generators (total=None) without errors."""
    # Generator with unknown length
    def gen():
        for i in range(4):
            yield i

    # Instantiate tqdm_rich with the generator
    pbar = tqdm_rich(gen(), desc="gen", leave=False, disable=False)
    # Iterate through the generator
    for _ in pbar:
        pass
    pbar.close()

    # The progress bar should have completed all iterations
    assert pbar.n == 4, "Progress bar did not complete all generator iterations"
    # The internal task should have been finished
    assert pbar._prog.finished, "Progress bar not marked as finished after generator close"
