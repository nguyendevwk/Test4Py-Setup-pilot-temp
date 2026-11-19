import pytest
from httpie.output.formatters.colors import make_styles
from pygments.style import Style

def test_make_styles_returns_dict_with_expected_keys_and_lists():
    styles = make_styles()
    # The keys should be the names from SHADE_TO_PIE_STYLE
    assert isinstance(styles, dict)
    # There should be at least one key
    assert styles, "make_styles returned an empty dict"
    for name, style_list in styles.items():
        # Each key should map to a list of two style classes
        assert isinstance(style_list, list)
        assert len(style_list) == 2
        # Each item should be a subclass of pygments.style.Style
        for style_cls in style_list:
            assert issubclass(style_cls, Style)

def test_style_classes_have_expected_attributes():
    styles = make_styles()
    for style_list in styles.values():
        for style_cls in style_list:
            # Instantiate the style to inspect attributes
            style_instance = style_cls()
            # Common pygments style attributes
            assert hasattr(style_instance, "background_color")
            assert hasattr(style_instance, "highlight_color")
            # The style should define a token style mapping
            assert isinstance(style_instance.style, dict)

def test_style_classes_are_unique_and_not_reused():
    styles = make_styles()
    all_style_classes = [cls for lst in styles.values() for cls in lst]
    # Ensure no duplicate class objects across the list
    assert len(all_style_classes) == len(set(all_style_classes))
