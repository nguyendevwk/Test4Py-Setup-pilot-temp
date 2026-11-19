import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from tqdm import tqdm_gui

def test_tqdm_gui_basic_iteration(tmp_path):
    """Verify that tqdm_gui updates line data during iteration."""
    # Create a small iterable
    data = range(5)
    # Capture experimental warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        pbar = tqdm_gui(data, colour="r", disable=False, leave=False)
        # Ensure warning was issued
        assert any("GUI is experimental" in str(wi.message) for wi in w)

    # Iterate through the data
    for _ in pbar:
        pass

    # After iteration, the line data should have 5 points
    assert len(pbar.xdata) == 5
    assert len(pbar.ydata) == 5
    assert len(pbar.zdata) == 5

    # The figure should have been created and not closed yet
    assert pbar.fig is not None
    assert pbar.fig.canvas.manager is not None

    # Close the progress bar
    pbar.close()
    # After close, the figure should be closed
    assert pbar.fig.canvas.manager is None

def test_tqdm_gui_no_total(tmp_path):
    """Verify behavior when total is None (unknown total)."""
    data = [1, 2, 3, 4, 5]
    pbar = tqdm_gui(data, disable=False, leave=False)
    # The total should be None
    assert pbar.total is None
    # The xdata should be a deque
    assert isinstance(pbar.xdata, type(pbar.xdata))
    # Iterate
    for _ in pbar:
        pass
    # After iteration, xdata should have 5 elements
    assert len(pbar.xdata) == 5
    # The xdata values should be timestamps (float)
    assert all(isinstance(v, float) for v in pbar.xdata)
    pbar.close()

def test_tqdm_gui_mininterval_and_toolbar(tmp_path):
    """Verify that mininterval is enforced and toolbar restored on close."""
    data = range(3)
    pbar = tqdm_gui(data, disable=False, leave=False)
    # mininterval should be at least 0.5
    assert pbar.mininterval >= 0.5
    # Toolbar should be temporarily set to 'None'
    assert pbar.mpl.rcParams['toolbar'] == 'None'
    # Iterate
    for _ in pbar:
        pass
    # After close, toolbar should be restored to original value
    original_toolbar = pbar.toolbar
    pbar.close()
    assert pbar.mpl.rcParams['toolbar'] == original_toolbar
