import pytest
import pygments.style
from httpie.output.formatters.colors import Solarized256Style

def test_solarized256_style_inherits_pygments_style():
    """Solarized256Style should be a subclass of pygments.style.Style."""
    assert issubclass(Solarized256Style, pygments.style.Style)

def test_solarized256_style_background_color():
    """The background_color attribute must match the defined BASE03 value."""
    expected = "#1c1c1c"
    assert Solarized256Style.background_color == expected

def test_solarized256_style_token_mappings():
    """The style's token mapping should contain specific expected entries."""
    # Pick a few representative tokens and their expected colors
    expected_mappings = {
        pygments.token.Keyword: "#5f8700",          # GREEN
        pygments.token.String: "#00afaf",           # CYAN
        pygments.token.Comment: "#4e4e4e",          # BASE01
        pygments.token.Name.Function: "#0087ff",    # BLUE
    }
    for token, color in expected_mappings.items():
        assert Solarized256Style.styles.get(token) == color
