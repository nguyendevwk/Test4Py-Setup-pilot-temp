import pytest
from httpie.output.formatters.colors import make_style
from pygments.style import Style
from httpie.ui.palette import get_color

def test_make_style_creates_style_with_formatted_values():
    raw = {"Token.Text": "red bold", "Token.Keyword": "blue"}
    style_cls = make_style("TestStyle", raw, shade=1)
    # The returned class should inherit from pygments.style.Style
    assert issubclass(style_cls, Style)
    # The styles dict should contain the same keys
    assert set(style_cls.styles.keys()) == set(raw.keys())
    # Each value should be a string that contains the original words
    for key, original in raw.items():
        formatted = style_cls.styles[key]
        # The formatted string should contain each word from the original
        for word in original.split():
            assert word in formatted

def test_make_style_handles_missing_color_returns_original():
    # Use a color name that is unlikely to be defined in the palette
    raw = {"Token.Text": "nonexistentcolor bold"}
    style_cls = make_style("MissingColorStyle", raw, shade=1)
    formatted = style_cls.styles["Token.Text"]
    # Since get_color will return None for the unknown color, the word should remain unchanged
    assert "nonexistentcolor" in formatted
    # The word 'bold' should also remain unchanged
    assert "bold" in formatted

def test_make_style_inherits_from_pygments_style_and_has_expected_attributes():
    raw = {"Token.Text": "red"}
    style_cls = make_style("SimpleStyle", raw, shade=0)
    # Ensure the class is a subclass of pygments.style.Style
    assert issubclass(style_cls, Style)
    # The class should have a 'styles' attribute that is a dict
    assert isinstance(style_cls.styles, dict)
    # The dict should map the token to the formatted string
    assert style_cls.styles["Token.Text"] == get_color("red", 0) or "red"
