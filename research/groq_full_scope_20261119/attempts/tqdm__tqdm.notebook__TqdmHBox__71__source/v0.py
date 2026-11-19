import pytest
from tqdm.notebook import TqdmHBox
from tqdm.std import tqdm as std_tqdm
from ipywidgets import HBox
import io
import sys

# Helper to create a TqdmHBox with a progress bar
def make_hbox(total=5, desc="test"):
    pbar = std_tqdm(total=total, desc=desc, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    hbox = TqdmHBox()
    hbox.pbar = pbar
    return hbox

def test_json_pretty_flag():
    hbox = make_hbox(total=3)
    # Advance progress to have some state
    hbox.pbar.update(1)
    # Default pretty=None should not modify ascii flag
    json_default = hbox._json_()
    assert "ascii" not in json_default
    # pretty=True should set ascii to False
    json_pretty = hbox._json_(pretty=True)
    assert json_pretty["ascii"] is False
    # pretty=False should set ascii to True
    json_not_pretty = hbox._json_(pretty=False)
    assert json_not_pretty["ascii"] is True

def test_repr_output_contains_progress():
    hbox = make_hbox(total=4, desc="demo")
    # Update progress to 2 out of 4
    hbox.pbar.update(2)
    repr_str = hbox.__repr__(pretty=False)
    # The representation should include the description and the progress numbers
    assert "demo" in repr_str
    assert "2/4" in repr_str
    # It should not contain the word 'ascii' because pretty=False
    assert "ascii" not in repr_str

def test_repr_pretty_writes_to_printer():
    hbox = make_hbox(total=2, desc="pretty")
    hbox.pbar.update(1)
    # Capture the output of the pretty printer
    buffer = io.StringIO()
    class DummyPretty:
        def text(self, s):
            buffer.write(s)
    dummy_pp = DummyPretty()
    hbox._repr_pretty_(dummy_pp)
    output = buffer.getvalue()
    # The output should match the __repr__ with pretty=True
    expected = hbox.__repr__(pretty=True)
    assert output == expected
