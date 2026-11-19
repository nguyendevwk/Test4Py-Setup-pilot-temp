import pytest
from httpie.output.formatters.colors import make_styles
from httpie.ui.palette import SHADE_TO_PIE_STYLE

def test_make_styles_keys_and_structure():
    """make_styles should return a dict with keys matching SHADE_TO_PIE_STYLE values."""
    styles = make_styles()
    # The keys should exactly match the values of SHADE_TO_PIE_STYLE
    assert set(styles.keys()) == set(SHADE_TO_PIE_STYLE.values())
    # Each key should map to a list of two style objects
    for key, style_list in styles.items():
        assert isinstance(style_list, list)
        assert len(style_list) == 2
        # Each style object should be a tuple (style_name, style_map, shade)
        for style in style_list:
            assert isinstance(style, tuple)
            assert len(style) == 3
            style_name, style_map, shade = style
            # style_name should be a string
            assert isinstance(style_name, str)
            # style_map should be a dict
            assert isinstance(style_map, dict)
            # shade should be one of the keys in SHADE_TO_PIE_STYLE
            assert shade in SHADE_TO_PIE_STYLE

def test_make_styles_consistency_across_shades():
    """Styles for different shades should be distinct objects."""
    styles = make_styles()
    # Collect all style objects
    all_styles = [style for style_list in styles.values() for style in style_list]
    # Ensure no two style objects are the same instance
    assert len(all_styles) == len(set(id(s) for s in all_styles))

def test_make_styles_error_on_missing_style():
    """If a style name is not found, make_style should raise ClassNotFound."""
    # Temporarily monkeypatch the internal make_style to raise ClassNotFound
    from httpie.output.formatters.colors import make_style
    original_make_style = make_style
    def fake_make_style(name, style_map, shade):
        raise ClassNotFound(name)
    try:
        # Replace the function in the module
        import httpie.output.formatters.colors as mod
        mod.make_style = fake_make_style
        with pytest.raises(ClassNotFound):
            make_styles()
    finally:
        # Restore original function
        mod.make_style = original_make_style
