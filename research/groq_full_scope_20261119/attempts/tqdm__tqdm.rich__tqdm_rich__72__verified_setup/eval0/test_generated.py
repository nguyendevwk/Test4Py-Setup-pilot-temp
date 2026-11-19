import warnings
import pytest
from tqdm.rich import tqdm_rich

# Test 1: Normal usage – progress updates and close works without errors
def test_tqdm_rich_basic_progress():
    with tqdm_rich(total=3, leave=False, disable=False) as p:
        # Ensure the internal rich Progress object is created
        assert hasattr(p, "_prog")
        # Iterate and check that internal counter matches
        for i in range(3):
            p.update(1)
            assert p.n == i + 1
    # After context exit, close should have been called and no exception raised
    assert not hasattr(p, "_prog") or p._prog is None

# Test 2: Disable flag – no warning should be emitted
def test_tqdm_rich_disable_no_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        with tqdm_rich(total=2, disable=True) as p:
            # No progress should be shown; internal _prog should not be created
            assert not hasattr(p, "_prog")
            # Update should be a no-op
            p.update(1)
            assert p.n == 0
    # No experimental warning should have been raised
    assert all("experimental" not in str(item.message) for item in w)

# Test 3: Reset behavior – total can be changed after reset
def test_tqdm_rich_reset_total():
    with tqdm_rich(total=4, leave=False) as p:
        for _ in range(2):
            p.update(1)
        # Reset to a new total
        p.reset(total=6)
        # After reset, internal counter should be zero
        assert p.n == 0
        # Update again and check that total is updated
        p.update(3)
        assert p.n == 3
        # The internal rich progress should reflect the new total
        assert p._prog.tasks[0].total == 6
