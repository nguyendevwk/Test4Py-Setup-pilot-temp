import pygments.token
import pygments.formatters.terminal256
import pytest
from httpie.output.formatters.colors import Solarized256Style


def test_style_inheritance_and_attributes():
    """Solarized256Style should inherit from pygments.style.Style and expose expected attributes."""
    assert issubclass(Solarized256Style, pygments.style.Style)
    # background_color must be defined and be a hex string
    assert isinstance(Solarized256Style.background_color, str)
    assert Solarized256Style.background_color.startswith("#")
    # styles dict must contain at least one mapping
    assert isinstance(Solarized256Style.styles, dict)
    assert len(Solarized256Style.styles) > 0
    # Check that a known token maps to the expected color
    expected_color = Solarized256Style.styles[pygments.token.Keyword]
    assert expected_color == Solarized256Style.GREEN


def test_token_color_mapping_consistency():
    """Each token in the style should map to a valid hex color string."""
    for token, color in Solarized256Style.styles.items():
        # The color should be a string starting with '#'
        assert isinstance(color, str)
        assert color.startswith("#")
        # The color should be a valid hex code of length 7
        assert len(color) == 7
        # Ensure the hex digits are valid
        int(color[1:], 16)  # will raise ValueError if not hex


def test_terminal256_formatter_uses_style():
    """Terminal256Formatter should be able to use Solarized256Style without errors."""
    formatter = pygments.formatters.terminal256.Terminal256Formatter(style=Solarized256Style)
    # Format a simple string with a keyword token to ensure style is applied
    lexer = pygments.lexers.get_lexer_by_name("python")
    tokens = list(pygments.lexers._tokenize(lexer, "def foo(): pass"))
    # The formatter should produce a non-empty string
    output = formatter.format(tokens)
    assert isinstance(output, str)
    assert output != ""
    # The output should contain ANSI escape codes (since Terminal256Formatter uses them)
    assert "\x1b[" in output
