import pytest
from httpie.output.formatters.colors import make_styles, SHADE_TO_PIE_STYLE, PIE_HEADER_STYLE, PIE_BODY_STYLE
import pygments.style

def test_make_styles_returns_dict_with_expected_keys():
    styles = make_styles()
    # SHADE_TO_PIE_STYLE maps shade names to style names
    expected_names = set(SHADE_TO_PIE_STYLE.values())
    assert set(styles.keys()) == expected_names
    # Each style name should map to a list of two style classes
    for name, style_list in styles.items():
        assert isinstance(style_list, list)
        assert len(style_list) == 2
        header_style, body_style = style_list
        # Names should match the pattern used in make_styles
        assert header_style.__name__ == f"Pie{name}HeaderStyle"
        assert body_style.__name__ == f"Pie{name}BodyStyle"
        # Both should be subclasses of pygments.style.Style
        assert issubclass(header_style, pygments.style.Style)
        assert issubclass(body_style, pygments.style.Style)

def test_style_classes_have_correct_styles_dict():
    styles = make_styles()
    # Pick one shade to inspect
    shade_name = next(iter(SHADE_TO_PIE_STYLE.values()))
    header_style, body_style = styles[shade_name]
    # The 'styles' attribute should be a dict mapping tokens to formatted strings
    assert hasattr(header_style, "styles") and isinstance(header_style.styles, dict)
    assert hasattr(body_style, "styles") and isinstance(body_style.styles, dict)
    # Check that all keys from the raw style dicts are present
    for key in PIE_HEADER_STYLE:
        assert key in header_style.styles
    for key in PIE_BODY_STYLE:
        assert key in body_style.styles
    # Ensure that the formatted string contains at least one color code
    # (ColorString objects are converted to strings like 'bold' or color names)
    sample_header_value = header_style.styles[next(iter(PIE_HEADER_STYLE))]
    assert isinstance(sample_header_value, str)
    assert len(sample_header_value) > 0

def test_make_styles_handles_empty_SHADE_TO_PIE_STYLE():
    # Temporarily replace SHADE_TO_PIE_STYLE with an empty dict
    original = SHADE_TO_PIE_STYLE.copy()
    try:
        SHADE_TO_PIE_STYLE.clear()
        styles = make_styles()
        assert styles == {}
    finally:
        SHADE_TO_PIE_STYLE.update(original)
