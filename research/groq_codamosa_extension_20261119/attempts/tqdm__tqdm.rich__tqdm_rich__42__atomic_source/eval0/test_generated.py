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
    # Iteration should still work but do nothing
    for _ in pbar:
        pass
    assert pbar.n == 5

def test_tqdm_rich_warning_and_options(tmp_path):
    """Check that the experimental warning is issued and options are set."""
    with pytest.warns(TqdmExperimentalWarning, match="rich is experimental/alpha"):
        pbar = tqdm_rich(total=2, leave=True, disable=False, options={"transient": True})
    # The transient option should be overridden by leave=True
    assert pbar._prog._options["transient"] is False
    # The progress should still run to completion
    for _ in pbar:
        pass
    assert pbar.n == 2
