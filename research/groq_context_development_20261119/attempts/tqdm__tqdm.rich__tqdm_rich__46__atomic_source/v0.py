import pytest
from tqdm.rich import tqdm_rich
from tqdm.std import TqdmExperimentalWarning
from rich.progress import Progress


def test_tqdm_rich_disable_no_warning(tmp_path):
    """When disable=True, the constructor should not emit a warning."""
    with pytest.warns(None) as record:
        bar = tqdm_rich(total=5, disable=True)
        # The bar should be disabled and not create a Progress instance
        assert bar.disable is True
        assert not hasattr(bar, "_prog")
    # No warnings should have been captured
    assert len(record) == 0
    bar.close()


def test_tqdm_rich_progress_updates(tmp_path):
    """The rich progress bar should update its internal task correctly."""
    bar = tqdm_rich(total=3, leave=False)
    # The Progress instance should be created
    assert isinstance(bar._prog, Progress)
    # The task id should be stored
    task_id = bar._task_id
    # Initially completed should be 0
    assert bar.n == 0
    # Iterate and check that the internal task is updated
    for i in range(3):
        bar.update(1)
        # The Progress task should reflect the new completed count
        task = bar._prog.tasks[task_id]
        assert task.completed == i + 1
    # After closing, the Progress should be exited
    bar.close()
    # The Progress instance should still exist but its tasks list should be empty
    assert len(bar._prog.tasks) == 0


def test_tqdm_rich_reset_and_total(tmp_path):
    """Resetting the bar should reset the internal Progress task and allow a new total."""
    bar = tqdm_rich(total=2, leave=False)
    bar.update(2)  # reach completion
    bar.close()
    # Reset with a new total
    bar.reset(total=4)
    # The internal Progress should have a new task with the new total
    assert bar.total == 4
    assert bar.n == 0
    # The Progress instance should still be active
    assert isinstance(bar._prog, Progress)
    # Update and check that the task reflects the new total
    bar.update(1)
    task = bar._prog.tasks[bar._task_id]
    assert task.total == 4
    assert task.completed == 1
    bar.close()
