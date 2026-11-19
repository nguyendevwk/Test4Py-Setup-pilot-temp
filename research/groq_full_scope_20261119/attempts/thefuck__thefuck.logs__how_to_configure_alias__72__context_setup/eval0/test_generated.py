import builtins
import types
import sys
import pytest
from thefuck.logs import how_to_configure_alias, color
from thefuck import conf

# Helper to capture printed output
@pytest.fixture
def captured_output():
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    yield sys.stdout
    sys.stdout = old_stdout

# Simple configuration details object
class DummyConfig:
    def __init__(self, content, path, reload, can_configure_automatically):
        self.content = content
        self.path = path
        self.reload = reload
        self.can_configure_automatically = can_configure_automatically

    def _asdict(self):
        return {
            "content": self.content,
            "path": self.path,
            "reload": self.reload,
        }

def test_how_to_configure_alias_no_details(captured_output):
    """When no configuration details are provided, only the basic message and link are printed."""
    how_to_configure_alias(None)
    output = captured_output.getvalue()
    assert "Seems like" in output
    assert "alias isn't configured" in output
    assert "More details - https://github.com/nvbn/thefuck#manual-installation" in output
    # No configuration-specific lines
    assert "Please put" not in output
    assert "Or run" not in output

def test_how_to_configure_alias_with_details_and_auto(captured_output):
    """When configuration details are provided and automatic configuration is possible,
    the function prints the detailed instructions and the auto-config line."""
    cfg = DummyConfig(
        content="alias fuck='thefuck --alias'",
        path="~/.bashrc",
        reload="source ~/.bashrc",
        can_configure_automatically=True,
    )
    how_to_configure_alias(cfg)
    output = captured_output.getvalue()
    # Basic message
    assert "Seems like" in output
    # Detailed instructions
    assert "Please put" in output
    assert cfg.content in output
    assert cfg.path in output
    assert cfg.reload in output
    # Auto-config line
    assert "Or run" in output
    assert "fuck" in output
    # Link
    assert "More details" in output

def test_color_function_respects_no_colors(monkeypatch, captured_output):
    """The color helper returns an empty string when colors are disabled."""
    # Disable colors
    monkeypatch.setattr(conf.settings, "no_colors", True)
    # Capture output of how_to_configure_alias with colors disabled
    cfg = DummyConfig(
        content="alias fuck='thefuck --alias'",
        path="~/.bashrc",
        reload="source ~/.bashrc",
        can_configure_automatically=False,
    )
    how_to_configure_alias(cfg)
    output = captured_output.getvalue()
    # No ANSI escape codes should appear
    assert "\x1b" not in output
    # The output should still contain the expected text
    assert "Please put" in output
    assert cfg.content in output
