import pytest
from tqdm.rich import tqdm_rich
from tqdm import TqdmExperimentalWarning


def test_tqdm_rich_normal_progress(tmp_path):
    """Verify that tqdm_rich updates its internal rich.Progress correctly."""
    # Create a tqdm_rich with a small total
    bar = tqdm_rich(total=3, leave=False, disable=False)
    # Iterate a few times
    for _ in range(3):
        bar.update()
    # After iteration, n should equal total
    assert bar.n == 3
    # The internal rich.Progress should have been created
    assert hasattr(bar, "_prog")
    # The task should have been added and updated
    assert hasattr(bar, "_task_id")
    # The progress bar should reflect completion
    bar.close()
    # After close, the rich.Progress should be exited
    assert not bar._prog._tasks  # tasks list should be empty after exit


def test_tqdm_rich_disable_skips_gui(tmp_path):
    """When disable=True, tqdm_rich should not create a rich.Progress."""
    bar = tqdm_rich(total=5, disable=True)
    # No rich.Progress should be created
    assert not hasattr(bar, "_prog")
    # Updating should not raise
    bar.update()
    assert bar.n == 1
    bar.close()
    # Still no rich.Progress
    assert not hasattr(bar, "_prog")


def test_tqdm_rich_invalid_progress_raises():
    """Passing a non-iterable progress argument should raise TypeError."""
    with pytest.raises(TypeError):
        tqdm_rich(progress="not a tuple")
