import builtins
import types
import pytest
from thefuck.logs import already_configured

class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def test_already_configured_prints_expected_output(capsys):
    cfg = DummyConfig(reload="thefuck reload")
    already_configured(cfg)
    captured = capsys.readouterr()
    expected = (
        "Seems like \x1b[1mfuck\x1b[0m alias already configured!\n"
        "For applying changes run \x1b[1mthefuck reload\x1b[0m or restart your shell."
    )
    assert captured.out.strip() == expected.strip()

def test_already_configured_with_empty_reload(capsys):
    cfg = DummyConfig(reload="")
    already_configured(cfg)
    captured = capsys.readouterr()
    expected = (
        "Seems like \x1b[1mfuck\x1b[0m alias already configured!\n"
        "For applying changes run \x1b[1m\x1b[0m or restart your shell."
    )
    assert captured.out.strip() == expected.strip()

def test_already_configured_missing_reload_attribute():
    cfg = types.SimpleNamespace()
    with pytest.raises(AttributeError):
        already_configured(cfg)
