import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from tqdm import tqdm_gui

def test_tqdm_gui_basic_progress(tmp_path):
    """Verify that tqdm_gui creates a figure and updates data for a finite iterable."""
    data = list(range(10))
    with tqdm_gui(data, colour="r", disable=False, leave=False) as pbar:
        for _ in pbar:
            pass
    # After completion, the figure should be closed (leave=False)
    assert not plt.fignum_exists(pbar.fig.number)
    # The internal data lists should have 10 entries
    assert len(pbar.xdata) == 10
    assert len(pbar.ydata) == 10
    assert len(pbar.zdata) == 10
    # The last xdata value should be 100.0 (percent)
    assert pytest.approx(pbar.xdata[-1], rel=1e-3) == 100.0

def test_tqdm_gui_infinite_iterable(tmp_path):
    """Verify that tqdm_gui handles an infinite iterable (total=None)."""
    import itertools
    infinite = itertools.count()
    with pytest.raises(StopIteration):
        # Limit the loop to 5 iterations to avoid infinite loop
        with tqdm_gui(infinite, total=None, disable=False, leave=False) as pbar:
            for _ in range(5):
                next(pbar)
    # After the loop, the figure should be closed
    assert not plt.fignum_exists(pbar.fig.number)
    # xdata should contain 5 timestamps
    assert len(pbar.xdata) == 5
    # Since total is None, xdata holds elapsed times, not percentages
    assert all(isinstance(t, float) for t in pbar.xdata)

def test_tqdm_gui_disable_flag(tmp_path):
    """Verify that disabling tqdm_gui skips GUI creation and does not raise errors."""
    data = [1, 2, 3]
    with tqdm_gui(data, disable=True, leave=False) as pbar:
        for _ in pbar:
            pass
    # When disabled, no figure should be created
    assert not hasattr(pbar, "fig")
    # The internal data structures should not exist
    assert not hasattr(pbar, "xdata")
    assert not hasattr(pbar, "ydata")
    assert not hasattr(pbar, "zdata")
