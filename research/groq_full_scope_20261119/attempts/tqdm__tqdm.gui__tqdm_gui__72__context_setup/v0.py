import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest
from tqdm import tqdm_gui

def test_tqdm_gui_basic_iteration(tmp_path):
    """Verify that tqdm_gui updates line data during iteration."""
    data = range(5)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        pbar = tqdm_gui(data, colour="r", disable=False, leave=False)
        # Ensure warning about experimental GUI is issued
        assert any("GUI is experimental" in str(wi.message) for wi in w)
    # After construction, figure should exist
    assert pbar.fig is not None
    # Iterate over the data
    for _ in pbar:
        pass
    # After iteration, line data should have 5 points
    assert len(pbar.line1.get_xdata()) == 5
    assert len(pbar.line1.get_ydata()) == 5
    # The title should contain the final progress string
    title = pbar.ax.get_title()
    assert "100%" in title or "5/5" in title
    # Clean up
    pbar.close()
    # Figure should be closed
    assert not plt.fignum_exists(pbar.fig.number)

def test_tqdm_gui_no_total(tmp_path):
    """Verify behavior when total is None (unknown length)."""
    data = (i for i in range(3))  # generator, total=None
    pbar = tqdm_gui(data, disable=False, leave=False)
    # Since total is None, xdata is a deque
    assert hasattr(pbar.xdata, "popleft")
    # Iterate
    for _ in pbar:
        pass
    # After iteration, xdata length should be 3
    assert len(pbar.xdata) == 3
    # The x-axis should be inverted (seconds)
    assert pbar.ax.get_xlim()[0] > pbar.ax.get_xlim()[1]
    # Clean up
    pbar.close()

def test_tqdm_gui_disable_and_close(tmp_path):
    """Verify that disabling the progress bar prevents GUI updates."""
    data = range(2)
    pbar = tqdm_gui(data, disable=True, leave=False)
    # With disable=True, no figure should be created
    assert pbar.fig is None
    # Iteration should be a no-op
    for _ in pbar:
        pass
    # Closing should not raise errors
    pbar.close()
