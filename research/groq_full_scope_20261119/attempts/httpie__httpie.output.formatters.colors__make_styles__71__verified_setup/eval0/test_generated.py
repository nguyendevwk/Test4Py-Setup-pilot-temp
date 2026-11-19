import pytest
import pygments.style
from httpie.output.formatters.colors import make_styles, SHADE_TO_PIE_STYLE


def test_make_styles_keys_match_shades():
    """The keys of the returned dict should match the style names in SHADE_TO_PIE_STYLE."""
    styles = make_styles()
    expected_keys = set(SHADE_TO_PIE_STYLE.values())
    assert set(styles.keys()) == expected_keys, (
        f"Expected keys {expected_keys}, got {set(styles.keys())}"
    )


def test_make_styles_style_objects():
    """Each value should be a list of two pygments style objects."""
    styles = make_styles()
    for name, style_list in styles.items():
        assert isinstance(style_list, list), f"{name} value is not a list"
        assert len(style_list) == 2, f"{name} list does not contain exactly two styles"
        for style in style_list:
            assert isinstance(
                style, pygments.style.Style
            ), f"Style in {name} is not a pygments.style.Style instance"


def test_make_styles_deterministic(tmp_path):
    """Calling make_styles multiple times should produce identical results."""
    first = make_styles()
    second = make_styles()
    # Compare the string representation of each style to avoid deep object comparison
    for key in first:
        first_repr = [repr(s) for s in first[key]]
        second_repr = [repr(s) for s in second[key]]
        assert first_repr == second_repr, f"Styles for {key} differ between calls"
