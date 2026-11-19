import pytest
from types import SimpleNamespace

# Import the target class
from tqdm.notebook import TqdmHBox

# Helper class mimicking a tqdm progress bar
class DummyBar:
    def __init__(self, total, desc=""):
        self.format_dict = {
            "n": 0,
            "total": total,
            "desc": desc,
            "ascii": True,
        }

    def format_meter(self, **kwargs):
        # Return a deterministic string based on format_dict and kwargs
        return f"{kwargs.get('desc', '')} {kwargs.get('n', 0)}/{kwargs.get('total', 0)}"

def test_repr_without_pbar_returns_super_repr():
    """When no pbar is attached, __repr__ falls back to HBox's representation."""
    hbox = TqdmHBox()
    # Ensure pbar is None
    assert getattr(hbox, "pbar", None) is None
    # The repr should contain the class name of the parent (ipywidgets.HBox)
    rep = repr(hbox)
    assert "HBox" in rep or "ipywidgets" in rep

def test_repr_with_pbar_returns_formatted_meter():
    """When a pbar is attached, __repr__ returns the formatted meter string."""
    hbox = TqdmHBox()
    dummy = DummyBar(total=10, desc="Test")
    hbox.pbar = dummy
    # Update format_dict to reflect progress
    dummy.format_dict.update({"n": 3, "total": 10, "desc": "Test"})
    rep = hbox.__repr__(pretty=False)
    # The representation should match DummyBar.format_meter output
    expected = dummy.format_meter(**dummy.format_dict)
    assert rep == expected

def test_json_pretty_flag_modifies_ascii_key():
    """The _json_ method should toggle the 'ascii' key based on the pretty flag."""
    hbox = TqdmHBox()
    dummy = DummyBar(total=5)
    hbox.pbar = dummy
    # Default ascii is True
    json_default = hbox._json_()
    assert json_default["ascii"] is True
    # When pretty=True, ascii should be False
    json_pretty = hbox._json_(pretty=True)
    assert json_pretty["ascii"] is False
    # When pretty=False, ascii should remain True
    json_not_pretty = hbox._json_(pretty=False)
    assert json_not_pretty["ascii"] is True
