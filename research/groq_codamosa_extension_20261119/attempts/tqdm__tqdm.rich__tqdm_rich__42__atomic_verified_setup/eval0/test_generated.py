import pytest
from tqdm.rich import tqdm_rich
from tqdm.std import TqdmExperimentalWarning
from rich.progress import Progress

def test_tqdm_rich_basic_progress(tmp_path):
    """Verify that tqdm_rich updates the internal rich Progress task."""
    # Create a tqdm_rich instance with a small total
    pbar = tqdm_rich(total=3, leave=False, disable=False)
    # Iterate through the progress bar
    for _ in pbar:
        pass
    # After completion, the internal task should be finished
    assert pbar.n == 3
    # The rich Progress instance should have a task with 100% completion
    task = pbar._prog._tasks[pbar._task_id]
    assert task.completed == 3
    # Ensure the description is updated correctly
    assert task.description == pbar.desc or ""

def test_tqdm_rich_disable_behavior():
    """When disable=True, tqdm_rich should not initialize the rich Progress."""
    pbar = tqdm_rich(total=5, disable=True)
    # The rich Progress instance should not exist
    assert not hasattr(pbar, "_prog")
    # Iterating should not raise errors and n should remain 0
    for _ in pbar:
        pass
    assert pbar.n == 0

def test_tqdm_rich_warning_and_options(tmp_path):
    """Check that the experimental warning is issued and options are set correctly."""
    with pytest.warns(TqdmExperimentalWarning, match="rich is experimental/alpha"):
        pbar = tqdm_rich(total=2, leave=False, options={"transient": True})
    # The transient option should be set to True
    assert pbar._prog._options["transient"] is True
    # The progress bar should still function
    for _ in pbar:
        pass
    assert pbar.n == 2
