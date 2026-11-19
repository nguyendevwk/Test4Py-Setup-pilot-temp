import pytest
from httpie.output.formatters.colors import make_style, get_color, AUTO_STYLE, SHADE_TO_PIE_STYLE
from pygments.style import Style

def test_make_style_formats_colors_correctly():
    # Define raw styles with a token that will be colored
    raw_styles = {
        "Token.Keyword": "bold red",
        "Token.Name": "italic green",
    }
    # Use a shade that exists in the palette to ensure get_color returns a ColorString
    shade = AUTO_STYLE
    style_cls = make_style("TestStyle", raw_styles, shade)

    # The returned class should inherit from pygments.style.Style
    assert issubclass(style_cls, Style)

    # The styles dict should be present and formatted
    formatted = style_cls.styles
    assert isinstance(formatted, dict)
    # Each value should be a string with color codes inserted
    for key, value in formatted.items():
        assert isinstance(value, str)
        # The value should contain the original words
        for part in raw_styles[key].split():
            assert part in value

def test_make_style_ignores_missing_colors():
    # Use a shade that is not present in the palette to force get_color to return None
    raw_styles = {
        "Token.Comment": "blue",
        "Token.String": "yellow",
    }
    shade = "nonexistent_shade"
    style_cls = make_style("NoColorStyle", raw_styles, shade)

    # The styles dict should contain the original values unchanged
    formatted = style_cls.styles
    assert formatted["Token.Comment"] == "blue"
    assert formatted["Token.String"] == "yellow"

def test_make_style_inherits_pygments_style_and_has_expected_attributes():
    raw_styles = {"Token.Error": "bold red"}
    shade = AUTO_STYLE
    style_cls = make_style("ErrorStyle", raw_styles, shade)

    # Ensure the class is a subclass of pygments.style.Style
    assert issubclass(style_cls, Style)

    # The class should have a 'styles' attribute that is a dict
    assert hasattr(style_cls, "styles")
    assert isinstance(style_cls.styles, dict)

    # The dict should contain the formatted style for the given token
    assert "Token.Error" in style_cls.styles
    # The formatted style should include the color code from the palette
    assert "red" in style_cls.styles["Token.Error"]
