import pytest
from tqdm.notebook import TqdmHBox
from tqdm import tqdm
from ipywidgets import HBox

def test_json_representation_pretty_and_ascii(tmp_path):
    # Create a simple tqdm progress bar with a known format
    pbar = tqdm(total=10, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    hbox = TqdmHBox()
    hbox.pbar = pbar

    # When pretty is None, ascii should be whatever the default is
    json_default = hbox._json_()
    assert isinstance(json_default, dict)
    assert "ascii" in json_default
    # ascii default is True for tqdm
    assert json_default["ascii"] is True

    # When pretty is True, ascii should be False
    json_pretty = hbox._json_(pretty=True)
    assert json_pretty["ascii"] is False

    # When pretty is False, ascii should be True
    json_ascii = hbox._json_(pretty=False)
    assert json_ascii["ascii"] is True

def test_repr_and_repr_pretty(tmp_path):
    # Create a progress bar with a custom format that includes the bar
    pbar = tqdm(total=5, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    hbox = TqdmHBox()
    hbox.pbar = pbar

    # __repr__ with default pretty=False should produce a string containing the bar
    repr_default = repr(hbox)
    assert isinstance(repr_default, str)
    assert "|" in repr_default  # bar separator
    assert "0/5" in repr_default  # initial state

    # __repr__ with pretty=True should produce a string with the bar and ascii=False
    repr_pretty = hbox.__repr__(pretty=True)
    assert isinstance(repr_pretty, str)
    assert "|" in repr_pretty
    assert "0/5" in repr_pretty

    # Ensure that the pretty representation is different from the default
    assert repr_default != repr_pretty

def test_repr_pretty_method_output(tmp_path):
    # Create a progress bar and attach to HBox
    pbar = tqdm(total=3, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}")
    hbox = TqdmHBox()
    hbox.pbar = pbar

    # Capture the output of the _repr_pretty_ method
    class DummyPrettyPrinter:
        def __init__(self):
            self.texts = []

        def text(self, txt):
            self.texts.append(txt)

    pp = DummyPrettyPrinter()
    hbox._repr_pretty_(pp)

    # The dummy printer should have received exactly one string
    assert len(pp.texts) == 1
    pretty_output = pp.texts[0]
    assert isinstance(pretty_output, str)
    assert "|" in pretty_output
    assert "0/3" in pretty_output
