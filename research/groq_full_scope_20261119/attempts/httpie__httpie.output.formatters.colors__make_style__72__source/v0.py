import pytest
from httpie.output.formatters.colors import make_style
from httpie.ui.palette import get_color
from pygments.style import Style

def test_make_style_formats_values_and_inherits_style():
    raw = {"Token.Text": "red bold", "Token.Keyword": "blue"}
    # Ensure that get_color returns a string for known colors
    assert get_color("red", "auto") is not None
    assert get_color("blue", "auto") is not None
    StyleClass = make_style("TestStyle", raw, "auto")
    # The class should inherit from pygments.style.Style
    assert issubclass(StyleClass, Style)
    # The styles dict should have the same keys
    assert set(StyleClass.styles.keys()) == set(raw.keys())
    # Each value should be formatted by get_color
    for key, value in raw.items():
        formatted = StyleClass.styles[key]
        # The formatted string should contain the color codes
        assert get_color(value.split()[0], "auto") in formatted

def test_make_style_ignores_unknown_colors():
    raw = {"Token.Text": "unknowncolor bold", "Token.Keyword": "anotherunknown"}
    StyleClass = make_style("UnknownColorStyle", raw, "auto")
    # get_color should return None for unknown colors
    assert get_color("unknowncolor", "auto") is None
    assert get_color("anotherunknown", "auto") is None
    # Therefore the formatted values should be unchanged
    assert StyleClass.styles["Token.Text"] == "unknowncolor bold"
    assert StyleClass.styles["Token.Keyword"] == "anotherunknown"

def test_make_style_handles_empty_and_single_token():
    raw = {"Token.Text": "", "Token.Keyword": "red"}
    StyleClass = make_style("EmptyStyle", raw, "auto")
    # Empty string should remain empty
    assert StyleClass.styles["Token.Text"] == ""
    # Single color should be formatted correctly
    assert get_color("red", "auto") in StyleClass.styles["Token.Keyword"]
