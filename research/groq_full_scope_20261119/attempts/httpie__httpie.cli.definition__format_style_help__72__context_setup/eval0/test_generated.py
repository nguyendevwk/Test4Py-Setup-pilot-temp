import pytest
from httpie.cli.definition import format_style_help
from httpie.output.formatters.colors import DEFAULT_STYLE, AUTO_STYLE, BUNDLED_STYLES

def test_format_style_help_default_behavior():
    """When isolation_mode is False, the help text contains the default style
    and lists the provided styles in the expected format."""
    styles = ["monokai", "solarized", "gruvbox"]
    help_text = format_style_help(styles, isolation_mode=False)
    # Default style should be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in help_text
    # Provided styles should appear, wrapped at 60 characters
    wrapped = "\n".join(
        f'    {line.strip()}'
        for line in __import__("textwrap").wrap(', '.join(styles), 60)
    ).strip()
    assert wrapped in help_text
    # No isolation mode instructions should be present
    assert "For finding out all available styles" not in help_text
    # Auto style description should be present
    assert f'The "{AUTO_STYLE}" style follows your terminal' in help_text

def test_format_style_help_isolation_mode():
    """When isolation_mode is True, the help text includes isolation instructions
    and lists only bundled styles sorted alphabetically."""
    help_text = format_style_help([], isolation_mode=True)
    # Isolation instructions should be present
    assert "For finding out all available styles in your system" in help_text
    # Bundled styles should be sorted and listed
    bundled_sorted = sorted(BUNDLED_STYLES)
    wrapped = "\n".join(
        f'    {line.strip()}'
        for line in __import__("textwrap").wrap(', '.join(bundled_sorted), 60)
    ).strip()
    assert wrapped in help_text
    # The default style should still be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in help_text

def test_format_style_help_empty_styles():
    """When an empty list of styles is provided, the function still returns a
    well‑formed string without errors and without listing any styles."""
    help_text = format_style_help([], isolation_mode=False)
    # No style names should appear in the list section
    assert "monokai" not in help_text
    assert "solarized" not in help_text
    # The available_styles placeholder should be empty
    assert "    " not in help_text.split("It can be one of:")[1]
    # The rest of the text should still be present
    assert "The" in help_text
