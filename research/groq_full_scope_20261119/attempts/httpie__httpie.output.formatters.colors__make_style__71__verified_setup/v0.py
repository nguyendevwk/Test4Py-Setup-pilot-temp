import pytest
from httpie.output.formatters.colors import make_style
from pygments.style import Style
from httpie.ui.palette import get_color

def test_make_style_basic_styles(tmp_path):
    # Define raw styles with simple color names
    raw = {"Token.Text": "red", "Token.Comment": "green bold"}
    # Use a shade that will be passed to get_color
    shade = "dark"
    # Create the style class
    StyleCls = make_style("TestStyle", raw, shade)
    # The class should inherit from pygments.style.Style
    assert issubclass(StyleCls, Style)
    # The styles dict should be present and formatted
    assert hasattr(StyleCls, "styles")
    # Each key should be preserved
    assert set(StyleCls.styles.keys()) == {"Token.Text", "Token.Comment"}
    # The values should be processed by get_color
    for key, value in raw.items():
        formatted = " ".join(get_color(part, shade) or part for part in value.split())
        assert StyleCls.styles[key] == formatted

def test_make_style_multiple_parts_and_none(tmp_path):
    # raw style with parts that may not have a color mapping
    raw = {"Token.Keyword": "blue italic", "Token.String": "unknown"}
    shade = "light"
    StyleCls = make_style("TestStyle2", raw, shade)
    # For "blue italic", get_color should return something for "blue" and None for "italic"
    formatted_keyword = " ".join(get_color(part, shade) or part for part in "blue italic".split())
    assert StyleCls.styles["Token.Keyword"] == formatted_keyword
    # For "unknown", get_color likely returns None, so original part is kept
    assert StyleCls.styles["Token.String"] == "unknown"

def test_make_style_invalid_input_raises_type_error():
    # make_style expects a dict; passing a list should raise a TypeError when iterating
    with pytest.raises(TypeError):
        make_style("BadStyle", ["not", "a", "dict"], "any")
