import pytest
from httpie.output.formatters.colors import make_style
from pygments.style import Style
from httpie.ui.palette import get_color

def test_make_style_creates_style_class_with_processed_values(tmp_path):
    raw = {"Token.Name": "red bold", "Token.Comment": "green italic"}
    style_cls = make_style("TestStyle", raw, shade="dark")
    # The returned object should be a subclass of pygments.style.Style
    assert issubclass(style_cls, Style)
    # The styles dict should contain the same keys
    assert set(style_cls.styles.keys()) == {"Token.Name", "Token.Comment"}
    # Each value should be processed by get_color for each part
    for key, value in raw.items():
        processed = style_cls.styles[key]
        # split original and processed parts
        original_parts = value.split()
        processed_parts = processed.split()
        # Each original part should either be unchanged or wrapped by get_color
        for op, pp in zip(original_parts, processed_parts):
            if get_color(op, "dark"):
                # wrapped part should contain the original part
                assert op in pp
            else:
                assert op == pp

def test_make_style_with_empty_raw_returns_empty_styles():
    style_cls = make_style("EmptyStyle", {}, shade="light")
    assert isinstance(style_cls.styles, dict)
    assert style_cls.styles == {}

def test_make_style_raises_type_error_on_invalid_raw_styles():
    with pytest.raises(TypeError):
        make_style("BadStyle", None, shade="light")
