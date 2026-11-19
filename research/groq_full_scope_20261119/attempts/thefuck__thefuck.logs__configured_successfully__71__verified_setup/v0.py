import builtins
import io
import sys
import pytest
from thefuck.logs import configured_successfully
from colorama import Style

class DummyConfig:
    def __init__(self, reload):
        self.reload = reload

def capture_stdout(func, *args, **kwargs):
    """Utility to capture stdout of a function call."""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

def test_configured_successfully_normal(tmp_path):
    """Test that the function prints the expected message with a normal reload command."""
    config = DummyConfig(reload="source ~/.bashrc")
    output = capture_stdout(configured_successfully, config)
    expected = (
        f"{Style.BRIGHT}fuck{Style.RESET_ALL} alias configured successfully!\n"
        f"For applying changes run {Style.BRIGHT}source ~/.bashrc{Style.RESET_ALL}"
        f" or restart your shell."
    )
    assert output == expected

def test_configured_successfully_empty_reload(tmp_path):
    """Test that the function handles an empty reload string gracefully."""
    config = DummyConfig(reload="")
    output = capture_stdout(configured_successfully, config)
    expected = (
        f"{Style.BRIGHT}fuck{Style.RESET_ALL} alias configured successfully!\n"
        f"For applying changes run {Style.BRIGHT}{Style.RESET_ALL}"
        f" or restart your shell."
    )
    assert output == expected

def test_configured_successfully_missing_reload():
    """Test that an AttributeError is raised when the configuration object lacks a reload attribute."""
    class IncompleteConfig:
        pass
    config = IncompleteConfig()
    with pytest.raises(AttributeError):
        configured_successfully(config)
