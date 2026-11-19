import pytest
from httpie.output.formatters.colors import make_style
from pygments.style import Style

def test_make_style_formats_colors_and_inherits():
    raw = {"Token.Keyword": "red bold", "Token.String": "green"}
    style_cls = make_style("TestStyle", raw, shade="dark")
    # The class should inherit from pygments.style.Style
    assert issubclass(style_cls, Style)
    # Instantiate and check the styles dict
    style_instance = style_cls()
    # The format_value function should replace color names with get_color output
    # Since we don't know the exact ColorString representation, we check that
    # the returned value contains the original color names or their replacements.
    for key, original in raw.items():
        formatted = style_instance.styles[key]
        # If get_color returned a ColorString, it will be converted to str
        # and should not be equal to the original plain string
        assert formatted != original
        # The formatted string should still contain the original color words
        # because get_color may return None for unknown colors
        for part in original.split():
            assert part in formatted or part in formatted.split()

def test_make_style_with_empty_dict_returns_empty_styles():
    style_cls = make_style("EmptyStyle", {}, shade=None)
    style_instance = style_cls()
    assert style_instance.styles == {}

def test_make_style_raises_type_error_on_invalid_raw_styles():
    with pytest.raises(TypeError):
        make_style("BadStyle", None, shade="light")
