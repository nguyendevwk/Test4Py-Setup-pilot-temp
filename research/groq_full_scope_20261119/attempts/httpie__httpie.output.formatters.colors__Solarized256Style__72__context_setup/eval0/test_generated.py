import pytest
import pygments.token
from httpie.output.formatters.colors import Solarized256Style

def test_style_background_and_inheritance():
    """Solarized256Style should inherit from pygments.style.Style and set the correct background."""
    assert issubclass(Solarized256Style, pygments.style.Style)
    assert Solarized256Style.background_color == "#1c1c1c"

def test_style_token_mappings():
    """Each token in the style's mapping should resolve to the expected color string."""
    # Pick a few representative tokens
    expected_mappings = {
        pygments.token.Keyword: "5f8700",
        pygments.token.String: "00afaf",
        pygments.token.Comment: "4e4e4e",
        pygments.token.Generic.Error: "af0000",
    }
    for token, expected_hex in expected_mappings.items():
        # The style stores hex strings; compare after stripping the leading '#'
        actual_hex = Solarized256Style.styles.get(token, None)
        assert actual_hex is not None, f"Token {token} missing in style mapping"
        assert actual_hex.lstrip('#') == expected_hex, f"Token {token} expected {expected_hex} got {actual_hex}"

def test_default_token_style():
    """Tokens not explicitly defined should default to BASE1 color."""
    # BASE1 is "#8a8a8a"
    default_color = Solarized256Style.styles.get(pygments.token.Token, None)
    assert default_color == "#8a8a8a", f"Default token color should be BASE1 (#8a8a8a), got {default_color}"
