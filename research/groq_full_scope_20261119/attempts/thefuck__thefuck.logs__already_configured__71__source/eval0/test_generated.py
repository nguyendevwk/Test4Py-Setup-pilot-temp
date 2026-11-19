import builtins
import io
import sys
import pytest
from thefuck.logs import already_configured

class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def test_already_configured_prints_expected_message(capsys):
    """Verify that the function prints the expected message with the reload command."""
    config = DummyConfig(reload="thefuck reload")
    already_configured(config)
    captured = capsys.readouterr()
    expected = (
        "Seems like fuck alias already configured!\n"
        "For applying changes run thefuck reload or restart your shell."
    )
    # The output may contain ANSI color codes; strip them for comparison
    stripped = "".join(
        ch for ch in captured.out if ch.isprintable() or ch in "\n\r"
    )
    assert stripped.strip() == expected.strip()

def test_already_configured_missing_reload_raises():
    """Calling with an object lacking a 'reload' attribute should raise AttributeError."""
    class Incomplete:
        pass
    with pytest.raises(AttributeError):
        already_configured(Incomplete())

def test_already_configured_with_empty_reload(capsys):
    """When reload is an empty string, the message should still be formatted correctly."""
    config = DummyConfig(reload="")
    already_configured(config)
    captured = capsys.readouterr()
    # Ensure the reload placeholder is present even if empty
    assert "For applying changes run  or restart your shell." in captured.out
