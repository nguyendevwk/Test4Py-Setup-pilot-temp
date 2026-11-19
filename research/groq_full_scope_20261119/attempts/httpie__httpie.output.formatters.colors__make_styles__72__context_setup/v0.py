import pytest
from httpie.output.formatters.colors import make_styles, SHADE_TO_PIE_STYLE
import pygments.style
import pygments.token

def test_make_styles_keys_and_structure():
    styles = make_styles()
    # Each shade name should be a key in the returned dict
    assert set(styles.keys()) == set(SHADE_TO_PIE_STYLE.keys())
    # Each value should be a list of two style classes
    for shade, style_list in styles.items():
        assert isinstance(style_list, list)
        assert len(style_list) == 2
        for style_cls in style_list:
            # Style classes should inherit from pygments.style.Style
            assert issubclass(style_cls, pygments.style.Style)
            # Each style class should have a 'styles' attribute
            assert hasattr(style_cls, 'styles')
            assert isinstance(style_cls.styles, dict)

def test_style_token_mapping_and_color_application():
    styles = make_styles()
    # Pick a known shade and its header style
    shade_name = next(iter(SHADE_TO_PIE_STYLE))
    header_style_cls = styles[shade_name][0]  # header style
    # The header style should map at least one token to a formatted string
    # For example, Name.Namespace should be bold and primary color
    token_key = pygments.token.Name.Namespace
    formatted = header_style_cls.styles.get(token_key)
    assert formatted is not None
    # The formatted string should contain the ANSI escape for bold
    assert 'bold' in formatted
    # It should also contain the ANSI escape for the primary color
    assert 'primary' in formatted

def test_style_uniqueness_and_consistency():
    styles = make_styles()
    # All style class names should be unique across all shades
    names = [cls.__name__ for shade in styles.values() for cls in shade]
    assert len(names) == len(set(names))
    # Recreating styles should yield the same class names
    styles_again = make_styles()
    names_again = [cls.__name__ for shade in styles_again.values() for cls in shade]
    assert names == names_again
