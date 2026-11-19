import pytest
from tqdm.notebook import TqdmHBox

class DummyPbar:
    """Minimal stand‑in for a tqdm progress bar."""
    def __init__(self):
        self.format_dict = {"n": 5, "total": 10, "ascii": True}
    def format_meter(self, **kwargs):
        # Return a deterministic string that includes the ascii flag
        return f"n={kwargs.get('n', 0)} total={kwargs.get('total', 0)} ascii={kwargs.get('ascii', True)}"

def test_json_pretty_flag_modifies_ascii(tmp_path):
    """_json_ should return the format_dict and toggle the ascii flag when pretty is set."""
    hbox = TqdmHBox()
    hbox.pbar = DummyPbar()
    # When pretty is True, ascii should be False
    json_pretty = hbox._json_(pretty=True)
    assert json_pretty["ascii"] is False
    # When pretty is False, ascii should remain True
    json_not_pretty = hbox._json_(pretty=False)
    assert json_not_pretty["ascii"] is True
    # The returned dict should contain the original keys
    assert set(json_pretty.keys()) == {"n", "total", "ascii"}

def test_repr_returns_formatted_meter(tmp_path):
    """__repr__ should delegate to the progress bar's format_meter."""
    hbox = TqdmHBox()
    hbox.pbar = DummyPbar()
    # The repr should match the string produced by DummyPbar.format_meter
    expected = "n=5 total=10 ascii=True"
    assert repr(hbox) == expected

def test_repr_pretty_none_returns_super_repr(tmp_path):
    """When no pbar is attached, __repr__ should fall back to the superclass representation."""
    hbox = TqdmHBox()
    # Ensure pbar is not set
    assert not hasattr(hbox, "pbar")
    # The representation should contain the class name and memory address
    rep = repr(hbox)
    assert rep.startswith("<tqdm.notebook.TqdmHBox")
    assert ">" in rep
