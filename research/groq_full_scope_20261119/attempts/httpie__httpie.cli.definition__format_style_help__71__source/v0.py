import pytest
from httpie.cli.definition import format_style_help
from httpie.output.formatters.colors import BUNDLED_STYLES, DEFAULT_STYLE, AUTO_STYLE

def test_format_style_help_default_behavior():
    # Provide a custom list of styles and verify the output contains them
    styles = ["monokai", "solarized", "dracula"]
    result = format_style_help(styles)
    # The default style should be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in result
    # The provided styles should appear in the output, each on a new line
    for style in styles:
        assert f'    {style}' in result
    # The auto style description should be present
    assert f'The "{AUTO_STYLE}" style follows your terminal\'s ANSI color styles.' in result
    # No isolation mode specific text should be present
    assert 'For finding out all available styles in your system' not in result

def test_format_style_help_isolation_mode():
    # When isolation_mode is True, the function should use BUNDLED_STYLES
    result = format_style_help([], isolation_mode=True)
    # The output should include the isolation mode header
    assert 'For finding out all available styles in your system' in result
    # All bundled styles should be listed, sorted alphabetically
    sorted_bundled = sorted(BUNDLED_STYLES)
    for style in sorted_bundled:
        assert f'    {style}' in result
    # The default style should still be referenced
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in result

def test_format_style_help_wrapping_and_spacing():
    # Provide a long list of styles to test text wrapping at 60 characters
    long_styles = [f"style{i}" for i in range(20)]
    result = format_style_help(long_styles)
    # The wrapped text should not exceed 60 characters per line after stripping
    for line in result.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('Output') and not stripped.startswith('The'):
            assert len(stripped) <= 60
    # Ensure no empty lines are introduced by wrapping
    assert '' not in [l.strip() for l in result.splitlines()]
