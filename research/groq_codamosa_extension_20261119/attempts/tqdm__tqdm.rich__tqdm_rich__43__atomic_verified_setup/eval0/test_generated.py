import pytest
from tqdm.rich import tqdm_rich
from rich.progress import Progress


def test_tqdm_rich_basic_progress(tmp_path):
    """Verify that tqdm_rich updates the rich Progress task correctly."""
    # Create a tqdm_rich instance with a small total
    bar = tqdm_rich(total=3, desc="test", leave=False, disable=False)
    # Ensure the underlying Progress object was created
    assert isinstance(bar._prog, Progress)
    # The task should start at 0 completed
    assert bar.n == 0
    # Iterate and check that the task updates
    for _ in range(3):
        bar.update(1)
    # After the loop, the task should be complete
    assert bar.n == 3
    # The rich Progress task should reflect the same completion
    task = bar._prog.tasks[bar._task_id]
    assert task.completed == 3
    # Closing should not raise
    bar.close()


def test_tqdm_rich_disable(tmp_path):
    """When disable=True, tqdm_rich should not create a Progress instance."""
    bar = tqdm_rich(total=5, desc="disabled", disable=True)
    # The internal _prog attribute should not exist
    assert not hasattr(bar, "_prog")
    # Updating should not raise an exception
    bar.update(1)
    assert bar.n == 1
    # Closing should not raise
    bar.close()


def test_tqdm_rich_invalid_progress_type(tmp_path):
    """Passing an invalid type for the progress argument should raise a TypeError."""
    with pytest.raises(TypeError):
        # The constructor expects a tuple of ProgressColumn objects; passing an int is invalid
        tqdm_rich(total=10, progress=42)
