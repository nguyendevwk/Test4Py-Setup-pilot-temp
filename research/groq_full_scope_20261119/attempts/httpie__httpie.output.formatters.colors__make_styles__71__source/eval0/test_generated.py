import pytest
from httpie.output.formatters import colors

def test_make_styles_keys_and_structure():
    """make_styles should return a dict with keys from SHADE_TO_PIE_STYLE."""
    styles = colors.make_styles()
    # SHADE_TO_PIE_STYLE is a mapping from shade to style name
    expected_keys = set(colors.SHADE_TO_PIE_STYLE.values())
    assert set(styles.keys()) == expected_keys, "Returned keys do not match SHADE_TO_PIE_STYLE values"

    # Each key maps to a list of two style tuples
    for key, value in styles.items():
        assert isinstance(value, list), f"Value for key {key} is not a list"
        assert len(value) == 2, f"Value list for key {key} does not contain exactly two items"
        for item in value:
            assert isinstance(item, tuple), f"Style item {item} for key {key} is not a tuple"
            # Each tuple should have at least two elements: style name and style map
            assert len(item) >= 2, f"Style tuple {item} for key {key} has fewer than two elements"

def test_make_styles_consistency_across_shades():
    """Styles for different shades should be distinct objects."""
    styles = colors.make_styles()
    # Collect all style tuples across all shades
    all_tuples = [t for sublist in styles.values() for t in sublist]
    # Ensure no duplicate tuples (by identity)
    assert len(all_tuples) == len(set(id(t) for t in all_tuples)), "Duplicate style tuples found across shades"

def test_make_styles_error_on_missing_style():
    """If a style name is missing, make_styles should raise an exception."""
    # Temporarily modify SHADE_TO_PIE_STYLE to include a non-existent style
    original = colors.SHADE_TO_PIE_STYLE.copy()
    colors.SHADE_TO_PIE_STYLE['missing'] = 'NonExistentStyle'
    try:
        with pytest.raises(Exception):
            colors.make_styles()
    finally:
        colors.SHADE_TO_PIE_STYLE.clear()
        colors.SHADE_TO_PIE_STYLE.update(original)
