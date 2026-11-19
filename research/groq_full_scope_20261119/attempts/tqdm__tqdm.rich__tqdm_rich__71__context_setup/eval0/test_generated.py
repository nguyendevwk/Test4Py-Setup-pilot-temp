import pytest
from tqdm.rich import tqdm_rich
from tqdm.std import TqdmExperimentalWarning

def test_tqdm_rich_basic_iteration(tmp_path):
    """Verify that tqdm_rich iterates correctly and updates internal counters."""
    data = list(range(5))
    bar = tqdm_rich(data, leave=False, disable=False)
    collected = []
    for item in bar:
        collected.append(item)
    # Ensure all items were yielded
    assert collected == data
    # The progress bar should have completed all iterations
    assert bar.n == len(data)
    # The internal rich task should reflect completion
    # (rich Progress updates are not directly accessible, but we can check that
    # the bar's display method does not raise an exception after completion)
    bar.display()
    bar.close()

def test_tqdm_rich_disable_flag(tmp_path):
    """When disable=True, the iterator should behave like a normal list."""
    data = [1, 2, 3]
    bar = tqdm_rich(data, disable=True)
    # The bar should not be a tqdm instance (no progress display)
    assert bar.disable is True
    # Iteration should yield the same items
    assert list(bar) == data
    # The internal counter should still track progress
    assert bar.n == len(data)

def test_tqdm_rich_warning_on_initialization(tmp_path):
    """Initializing tqdm_rich should emit a TqdmExperimentalWarning."""
    with pytest.warns(TqdmExperimentalWarning, match="rich is experimental/alpha"):
        bar = tqdm_rich([1, 2], leave=False, disable=False)
    # Ensure the bar is usable after warning
    assert list(bar) == [1, 2]
    bar.close()
