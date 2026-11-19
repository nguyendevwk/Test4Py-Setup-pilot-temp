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

    # The figure should still exist
    assert pbar.fig is not None
    # The title should contain the final progress string
    title = pbar.ax.get_title()
    assert "100%" in title or "5/5" in title

    # Clean up
    pbar.close()
    # After close, the figure should be closed
    assert not plt.fignum_exists(pbar.fig.number)

def test_tqdm_gui_no_total(tmp_path):
    """Verify behavior when total is None (unknown length)."""
    # Use an iterator without known length
    data = (i for i in range(3))
    pbar = tqdm_gui(data, disable=False, leave=False)

    # Iterate
    for _ in pbar:
        pass

    # For unknown total, xdata holds elapsed times
    assert all(isinstance(t, float) for t in pbar.xdata)
    # ydata and zdata should have 3 entries
    assert len(pbar.ydata) == 3
    assert len(pbar.zdata) == 3

    # The x-axis should be inverted
    assert pbar.ax.get_xlim()[0] > pbar.ax.get_xlim()[1]

    pbar.close()
    assert not plt.fignum_exists(pbar.fig.number)

def test_tqdm_gui_close_restores_toolbar(tmp_path):
    """Ensure that close restores the original toolbar setting."""
    # Record original toolbar
    original_toolbar = matplotlib.rcParams['toolbar']
    # Create a progress bar
    pbar = tqdm_gui(range(2), disable=False, leave=False)
    # Toolbar should be set to 'None' during operation
    assert matplotlib.rcParams['toolbar'] == 'None'
    # Close the progress bar
    pbar.close()
    # Toolbar should be restored
    assert matplotlib.rcParams['toolbar'] == original_toolbar
    # The figure should be closed
    assert not plt.fignum_exists(pbar.fig.number)
