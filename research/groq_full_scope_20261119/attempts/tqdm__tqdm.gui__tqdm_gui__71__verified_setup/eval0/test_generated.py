import matplotlib
matplotlib.use("Agg")  # use non‑interactive backend for tests
import pytest
from tqdm import tqdm_gui
from collections import deque
import time

def test_tqdm_gui_basic_progress(tmp_path):
    """Verify that tqdm_gui updates the figure and line data for a known total."""
    data = list(range(10))
    pbar = tqdm_gui(data, colour="r", leave=False, disable=False)
    # initial state
    assert pbar.total == 10
    assert isinstance(pbar.xdata, list)
    assert isinstance(pbar.ydata, list)
    assert isinstance(pbar.zdata, list)
    assert pbar.fig is not None
    assert pbar.ax is not None

    # iterate through the data
    for _ in pbar:
        pass

    # after iteration, the progress bar should be complete
    assert pbar.n == 10
    # xdata should contain 10 entries (percent values)
    assert len(pbar.xdata) == 10
    # ydata and zdata should have the same length
    assert len(pbar.ydata) == 10
    assert len(pbar.zdata) == 10
    # the last xdata entry should be 100.0
    assert pbar.xdata[-1] == 100.0

    # closing should not raise
    pbar.close()
    # after close, the figure should be closed
    assert not pbar.fig.canvas.manager._is_mpl_gui

def test_tqdm_gui_unknown_total(tmp_path):
    """Verify that tqdm_gui handles iterables with unknown length gracefully."""
    # create a generator (unknown length)
    def gen():
        for i in range(5):
            yield i
    pbar = tqdm_gui(gen(), colour="g", leave=False, disable=False)
    # total should be None
    assert pbar.total is None
    # xdata, ydata, zdata should be deques
    assert isinstance(pbar.xdata, deque)
    assert isinstance(pbar.ydata, deque)
    assert isinstance(pbar.zdata, deque)

    # iterate
    for _ in pbar:
        pass

    # after iteration, n should be 5
    assert pbar.n == 5
    # deques should contain 5 entries
    assert len(pbar.xdata) == 5
    assert len(pbar.ydata) == 5
    assert len(pbar.zdata) == 5

    # close without error
    pbar.close()

def test_tqdm_gui_disable_behavior(tmp_path):
    """Verify that disabling the progress bar prevents any GUI updates."""
    data = [1, 2, 3]
    pbar = tqdm_gui(data, colour="b", leave=False, disable=True)
    # When disabled, no figure should be created
    assert pbar.fig is None
    assert pbar.ax is None
    # Iterating should not raise
    for _ in pbar:
        pass
    # n should still count iterations
    assert pbar.n == 3
    # close should be a no‑op
    pbar.close()
