import warnings
import pytest
from tqdm.rich import tqdm_rich
from tqdm.std import TqdmExperimentalWarning

def test_tqdm_rich_normal_progress(tmp_path):
    """Verify that tqdm_rich updates progress and emits the experimental warning."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bar = tqdm_rich(total=3, desc="test")
        # iterate a few steps
        for _ in range(3):
            bar.update(1)
        bar.close()
    # The warning should be emitted once
    assert any(item.category is TqdmExperimentalWarning for item in w)
    # After close, the bar should have completed
    assert bar.n == 3
    assert bar.total == 3

def test_tqdm_rich_disable_no_gui(tmp_path):
    """When disable=True, the GUI should not be initialized and no warning emitted."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bar = tqdm_rich(total=2, disable=True)
        # No GUI should be created; _prog attribute should not exist
        assert not hasattr(bar, "_prog")
        # No warning should be emitted
        assert all(item.category is not TqdmExperimentalWarning for item in w)
        bar.close()
    # The bar should still track progress correctly
    assert bar.n == 0
    assert bar.total == 2

def test_tqdm_rich_invalid_progress_type():
    """Passing an invalid type for the progress argument should raise a TypeError."""
    with pytest.raises(TypeError):
        tqdm_rich(progress="not a tuple")
