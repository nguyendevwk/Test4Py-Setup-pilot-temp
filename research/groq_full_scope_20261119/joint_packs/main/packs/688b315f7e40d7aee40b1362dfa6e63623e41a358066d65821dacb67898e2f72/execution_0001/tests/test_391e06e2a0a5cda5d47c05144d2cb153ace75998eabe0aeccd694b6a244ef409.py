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
    # No isolation mode specific sections
    assert "For finding out all available styles" not in help_text
    # Auto style description present
    assert f'The "{AUTO_STYLE}" style follows your terminal' in help_text

def test_format_style_help_isolation_mode():
    """When isolation_mode is True, the help text includes the isolation
    instructions and lists only bundled styles sorted alphabetically."""
    help_text = format_style_help([], isolation_mode=True)
    # Isolation instructions should be present
    assert "For finding out all available styles in your system" in help_text
    # The list of styles should be sorted BUNDLED_STYLES
    sorted_bundled = "\n".join(
        f'    {line.strip()}'
        for line in __import__("textwrap").wrap(', '.join(sorted(BUNDLED_STYLES)), 60)
    ).strip()
    assert sorted_bundled in help_text
    # Default style still mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in help_text

def test_format_style_help_empty_styles():
    """When an empty list is provided and isolation_mode is False, the
    function should still produce a valid help string without errors."""
    help_text = format_style_help([], isolation_mode=False)
    # Should not contain any style names
    assert "monokai" not in help_text
    # Still contains default and auto style descriptions
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in help_text
    assert f'The "{AUTO_STYLE}" style follows your terminal' in help_text
