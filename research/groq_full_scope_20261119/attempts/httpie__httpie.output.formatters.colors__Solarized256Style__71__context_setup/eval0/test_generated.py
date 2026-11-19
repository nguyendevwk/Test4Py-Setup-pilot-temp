import pygments.token
import pytest
from httpie.output.formatters.colors import Solarized256Style


def test_solarized256style_background_color():
    """The style should expose the expected background color."""
    assert Solarized256Style.background_color == "#1c1c1c"


def test_solarized256style_token_mappings():
    """Specific token types must map to the correct color codes."""
    style = Solarized256Style
    # Keyword tokens
    assert style.styles[pygments.token.Keyword] == "#5f8700"  # GREEN
    assert style.styles[pygments.token.Keyword.Constant] == "#d75f00"  # ORANGE
    # String tokens
    assert style.styles[pygments.token.String] == "#00afaf"  # CYAN
    # Comment tokens
    assert style.styles[pygments.token.Comment] == "#4e4e4e"  # BASE01
    # Number tokens
    assert style.styles[pygments.token.Number] == "#00afaf"  # CYAN


def test_solarized256style_inherits_from_pygments_style():
    """The style class must be a subclass of pygments.style.Style."""
    assert issubclass(Solarized256Style, pygments.style.Style)
