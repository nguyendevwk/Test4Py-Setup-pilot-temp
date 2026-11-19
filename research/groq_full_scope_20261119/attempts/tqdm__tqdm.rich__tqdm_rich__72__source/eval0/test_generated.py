import warnings
import pytest
from tqdm.rich import tqdm_rich

# Test that disabling the progress bar skips GUI creation and does not raise warnings
def test_tqdm_rich_disable(tmp_path):
    with pytest.warns(None) as record:
        bar = tqdm_rich(total=5, disable=True, leave=False)
        # No warning should be emitted
        assert len(record) == 0
        # The bar should not have a _prog attribute
        assert not hasattr(bar, "_prog")
        # Iterating should not raise errors
        for _ in bar:
            pass
    # After iteration, close should be a no-op
    bar.close()

# Test that the progress bar updates correctly and displays the final state
def test_tqdm_rich_progress_update(tmp_path):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bar = tqdm_rich(total=3, leave=False)
        # A warning about experimental status should be emitted
        assert any("experimental" in str(warning.message).lower() for warning in w)
        # The bar should have a _prog attribute
        assert hasattr(bar, "_prog")
        # Iterate and check that internal counter matches
        for i, _ in enumerate(bar):
            assert bar.n == i + 1
        # After loop, bar.n should equal total
        assert bar.n == 3
        # Closing should not raise
        bar.close()

# Test that resetting the bar works and the internal state is cleared
def test_tqdm_rich_reset(tmp_path):
    bar = tqdm_rich(total=2, leave=False)
    for _ in bar:
        pass
    # After completion, n should be 2
    assert bar.n == 2
    # Reset with a new total
    bar.reset(total=4)
    # n should be reset to 0
    assert bar.n == 0
    # Iterate again and check new total
    for _ in bar:
        pass
    assert bar.n == 4
    bar.close()
