import pytest
from tqdm.notebook import TqdmHBox
from tqdm import tqdm

def test_json_pretty_returns_correct_dict(tmp_path):
    """TqdmHBox._json_ should return a dict with ascii flag set appropriately."""
    pbar = tqdm(total=5, leave=False)
    hbox = TqdmHBox()
    hbox.pbar = pbar
    # When pretty is True, ascii should be False
    json_pretty = hbox._json_(pretty=True)
    assert isinstance(json_pretty, dict)
    assert json_pretty.get("ascii") is False
    # When pretty is False, ascii should be True
    json_not_pretty = hbox._json_(pretty=False)
    assert json_not_pretty.get("ascii") is True
    # The dict should contain the same keys as the format_dict
    for key in pbar.format_dict:
        assert key in json_pretty

def test_repr_returns_meter_string(tmp_path):
    """TqdmHBox.__repr__ should return the formatted meter string."""
    pbar = tqdm(total=3, leave=False)
    hbox = TqdmHBox()
    hbox.pbar = pbar
    # Advance the bar to a known state
    pbar.update(1)
    repr_str = hbox.__repr__(pretty=False)
    # The string should contain the current progress and total
    assert "1/3" in repr_str
    # It should not contain the word 'ascii' because pretty=False
    assert "ascii" not in repr_str

def test_repr_pretty_uses_pretty_repr(tmp_path):
    """TqdmHBox._repr_pretty_ should delegate to __repr__ with pretty=True."""
    pbar = tqdm(total=2, leave=False)
    hbox = TqdmHBox()
    hbox.pbar = pbar
    pbar.update(1)
    # Capture the pretty representation via the rich pretty printer
    from rich.pretty import Pretty
    pretty_obj = Pretty(hbox)
    # The pretty printer will call _repr_pretty_
    # We assert that the resulting string contains the pretty meter
    # which should include the ascii flag set to False
    rendered = pretty_obj.__repr__()
    assert "1/2" in rendered
    assert "ascii" not in rendered
