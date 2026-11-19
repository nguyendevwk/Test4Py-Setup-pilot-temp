import pytest
from httpie.cli.definition import format_style_help
from httpie.output.formatters.colors import DEFAULT_STYLE, AUTO_STYLE, BUNDLED_STYLES

def test_format_style_help_normal():
    # Use a small set of styles to keep output predictable
    styles = ["monokai", "solarized", "gruvbox"]
    result = format_style_help(styles)
    # Default style should be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in result
    # Auto style description should be present
    assert f'The "{AUTO_STYLE}" style follows your terminal\'s ANSI color styles.' in result
    # All provided styles should appear in the wrapped list
    for style in styles:
        assert f'    {style}' in result
    # Isolation mode specific text should not be present
    assert 'For finding out all available styles in your system' not in result

def test_format_style_help_isolation_mode():
    # In isolation mode, the function should use BUNDLED_STYLES and add extra text
    result = format_style_help([], isolation_mode=True)
    # The isolation mode header should be present
    assert 'For finding out all available styles in your system' in result
    # The list should contain all bundled styles sorted
    for style in sorted(BUNDLED_STYLES):
        assert f'    {style}' in result
    # The default and auto style descriptions should still be present
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in result
    assert f'The "{AUTO_STYLE}" style follows your terminal\'s ANSI color styles.' in result

def test_format_style_help_wrapping_long_names():
    # Create a long style name to force wrapping
    long_style = "this_is_a_very_long_style_name_that_exceeds_sixty_characters_in_length"
    styles = [long_style, "short"]
    result = format_style_help(styles)
    # The long style should appear wrapped across multiple lines
    assert long_style in result
    # Ensure that the output does not contain a single line longer than 60 characters
    for line in result.splitlines():
        # Strip leading spaces used for indentation
        stripped = line.lstrip()
        if stripped:
            assert len(stripped) <= 60
