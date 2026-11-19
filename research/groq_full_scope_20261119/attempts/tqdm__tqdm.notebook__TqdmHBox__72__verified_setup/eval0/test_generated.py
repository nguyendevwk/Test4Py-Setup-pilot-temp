import io
import pytest
from tqdm.notebook import TqdmHBox
from tqdm.std import tqdm as std_tqdm
from ipywidgets import HBox


def test_json_pretty_flag(tmp_path):
    """_json_ should toggle the 'ascii' key based on the pretty flag."""
    # Create a dummy HBox with a tqdm progress bar
    hbox = TqdmHBox()
    hbox.pbar = std_tqdm(range(10), total=10, leave=False)
    # Force a single update to populate format_dict
    hbox.pbar.update(1)

    # Default call: pretty=None, ascii should be True (default)
    json_default = hbox._json_()
    assert json_default["ascii"] is True

    # pretty=True: ascii should be False
    json_pretty = hbox._json_(pretty=True)
    assert json_pretty["ascii"] is False

    # pretty=False: ascii should be True
    json_not_pretty = hbox._json_(pretty=False)
    assert json_not_pretty["ascii"] is True


def test_repr_without_pbar():
    """__repr__ should fall back to HBox's repr when no progress bar is set."""
    hbox = TqdmHBox()
    # Ensure no pbar attribute
    assert not hasattr(hbox, "pbar")
    # The representation should be the same as HBox's __repr__
    expected = super(TqdmHBox, hbox).__repr__()
    assert hbox.__repr__() == expected


def test_repr_with_pbar_and_pretty(tmp_path):
    """__repr__ should delegate to tqdm's format_meter when a pbar is present."""
    hbox = TqdmHBox()
    hbox.pbar = std_tqdm(range(5), total=5, leave=False)
    # Update to set internal state
    hbox.pbar.update(2)

    # Capture the representation
    repr_str = hbox.__repr__(pretty=True)
    # It should contain the progress bar text (e.g., '2/5')
    assert "2/5" in repr_str

    # _repr_pretty_ should write the same string to the pretty printer
    pretty_output = io.StringIO()
    class DummyPrettyPrinter:
        def __init__(self, stream):
            self.stream = stream
        def text(self, txt):
            self.stream.write(txt)
    pp = DummyPrettyPrinter(pretty_output)
    hbox._repr_pretty_(pp)
    assert pretty_output.getvalue() == repr_str
