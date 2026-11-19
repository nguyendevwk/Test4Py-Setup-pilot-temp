import sys
import io
import pytest
from thefuck.logs import already_configured
from colorama import Style

class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def test_already_configured_prints_expected_message(tmp_path):
    """Verify that the function prints the expected message with the reload command."""
    config = DummyConfig(reload="thefuck reload")
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        already_configured(config)
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    assert "Seems like" in output
    assert "alias already configured!" in output
    assert "For applying changes run" in output
    assert "thefuck reload" in output
    # Ensure color codes are present
    assert Style.BRIGHT in output
    assert Style.RESET_ALL in output

def test_already_configured_with_empty_reload(tmp_path):
    """When reload is an empty string, the message still contains the placeholder."""
    config = DummyConfig(reload="")
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        already_configured(config)
    finally:
        sys.stdout = sys_stdout
    output = captured.getvalue()
    assert "For applying changes run" in output
    # The reload placeholder should be empty but the surrounding text remains
    assert output.strip().endswith("or restart your shell.")

def test_already_configured_missing_reload_attribute():
    """If the configuration object lacks a 'reload' attribute, an AttributeError is raised."""
    class IncompleteConfig:
        pass
    config = IncompleteConfig()
    with pytest.raises(AttributeError):
        already_configured(config)
