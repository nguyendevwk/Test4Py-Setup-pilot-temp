import pytest
from tqdm.rich import tqdm_rich
from tqdm import tqdm as std_tqdm

# --------------------------------------------------------------------------- #
# Test 1: Normal operation – progress bar updates correctly for a small list
# --------------------------------------------------------------------------- #
def test_tqdm_rich_progress_updates(tmp_path):
    data = list(range(5))
    # Instantiate tqdm_rich with a short iterable
    with tqdm_rich(data, leave=False, disable=False) as pbar:
        # The rich Progress instance should be created
        assert hasattr(pbar, "_prog")
        # The task id should be set
        assert hasattr(pbar, "_task_id")
        # Initially, no items processed
        assert pbar.n == 0
        # Iterate through the data
        for _ in pbar:
            pass
        # After iteration, all items processed
        assert pbar.n == len(data)
        # The internal task should reflect the completed count
        task = pbar._prog._tasks[pbar._task_id]
        assert task.completed == len(data)
    # After exiting the context manager, the rich Progress should be closed
    # The _prog attribute should still exist but the task should be removed
    assert not pbar._prog._tasks  # no remaining tasks

# --------------------------------------------------------------------------- #
# Test 2: Disable flag – GUI should not be created and no errors raised
# --------------------------------------------------------------------------- #
def test_tqdm_rich_disable_flag():
    data = [1, 2, 3]
    # Instantiate with disable=True; no rich GUI should be created
    pbar = tqdm_rich(data, disable=True)
    # The _prog attribute should not exist because GUI is disabled
    assert not hasattr(pbar, "_prog")
    # Iteration should still work like a normal tqdm
    for _ in pbar:
        pass
    assert pbar.n == len(data)
    # Closing should be a no-op
    pbar.close()
    # No exception should have been raised during close

# --------------------------------------------------------------------------- #
# Test 3: Reset behavior – total can be changed and counter resets
# --------------------------------------------------------------------------- #
def test_tqdm_rich_reset_behavior():
    data = [1, 2, 3]
    pbar = tqdm_rich(data, total=10, disable=False)
    # Process two items
    for _ in pbar:
        if pbar.n == 2:
            break
    assert pbar.n == 2
    # Reset with a new total
    pbar.reset(total=5)
    # After reset, counter should be zero and total updated
    assert pbar.n == 0
    assert pbar.total == 5
    # Continue iterating to the new total
    for _ in pbar:
        pass
    assert pbar.n == 5
    pbar.close()
