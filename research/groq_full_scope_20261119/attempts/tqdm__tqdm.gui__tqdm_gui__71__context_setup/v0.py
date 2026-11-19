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
    data = itertools.count()
    with pytest.raises(StopIteration):
        with tqdm_gui(data, colour="g", disable=False, leave=False, maxiter=5) as pbar:
            for _ in pbar:
                pass
    # After stopping, the figure should be closed
    assert not plt.fignum_exists(pbar.fig.number)
    # The xdata should contain timestamps (not None)
    assert all(isinstance(t, float) for t in pbar.xdata)
    # The ydata and zdata should have the same length
    assert len(pbar.ydata) == len(pbar.zdata)

def test_tqdm_gui_disable(tmp_path):
    """Verify that disabling tqdm_gui skips GUI creation and does not raise errors."""
    data = [1, 2, 3]
    with tqdm_gui(data, disable=True, leave=False) as pbar:
        for _ in pbar:
            pass
    # When disabled, no figure should be created
    assert not hasattr(pbar, "fig")
    # The internal data structures should be empty
    assert pbar.xdata == []
    assert pbar.ydata == []
    assert pbar.zdata == []
