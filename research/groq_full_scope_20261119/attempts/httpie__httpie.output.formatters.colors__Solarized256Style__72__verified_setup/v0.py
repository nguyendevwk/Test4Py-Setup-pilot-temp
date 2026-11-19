import pytest
import pygments.token
from httpie.output.formatters.colors import Solarized256Style

def test_style_inherits_pygments_style():
    """Solarized256Style should be a subclass of pygments.style.Style."""
    assert issubclass(Solarized256Style, pygments.style.Style)

def test_background_color_and_base_constants():
    """The style defines a background_color and base constants correctly."""
    # background_color should match BASE03
    assert Solarized256Style.background_color == Solarized256Style.BASE03
    # Check that all BASE constants are hex strings of length 7 starting with '#'
    for name in dir(Solarized256Style):
        if name.startswith("BASE") and name.isupper():
            value = getattr(Solarized256Style, name)
            assert isinstance(value, str)
            assert value.startswith("#") and len(value) == 7

def test_styles_mapping_contains_expected_tokens():
    """The styles mapping should contain specific token types with correct color codes."""
    styles = Solarized256Style.styles
    # Keyword tokens should map to GREEN
    assert styles[pygments.token.Keyword] == Solarized256Style.GREEN
    # String tokens should map to CYAN
    assert styles[pygments.token.String] == Solarized256Style.CYAN
    # Comment tokens should map to BASE01
    assert styles[pygments.token.Comment] == Solarized256Style.BASE01
    # Generic.Error should map to RED
    assert styles[pygments.token.Generic.Error] == Solarized256Style.RED
