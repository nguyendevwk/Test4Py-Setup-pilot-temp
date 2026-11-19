import pytest
from httpie.cli.definition import format_style_help
from httpie.output.formatters.colors import DEFAULT_STYLE, AUTO_STYLE, BUNDLED_STYLES

def test_format_style_help_normal():
    # Provide a small list of styles
    styles = ["monokai", "solarized-dark", "gruvbox"]
    result = format_style_help(styles)
    # The default style should be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in result
    # The auto style should be referenced
    assert f'The "{AUTO_STYLE}" style follows your terminal' in result
    # All provided styles should appear in the wrapped list
    for style in styles:
        assert f'    {style}' in result
    # The isolation mode block should not be present
    assert 'For finding out all available styles in your system' not in result

def test_format_style_help_isolation_mode():
    # Use a custom list; isolation_mode should override it with bundled styles
    custom_styles = ["custom1", "custom2"]
    result = format_style_help(custom_styles, isolation_mode=True)
    # The isolation mode header should be present
    assert 'For finding out all available styles in your system' in result
    # The custom styles should not appear
    for style in custom_styles:
        assert style not in result
    # All bundled styles should appear, sorted
    for style in sorted(BUNDLED_STYLES):
        assert f'    {style}' in result

def test_format_style_help_empty_list():
    # Edge case: empty list of styles
    result = format_style_help([])
    # The available styles section should be empty but formatted correctly
    assert 'Output coloring style (default is "' in result
    # No style names should appear
    for line in result.splitlines():
        if line.strip().startswith('    '):
            assert line.strip() == ''
    # The auto style reference should still be present
    assert f'The "{AUTO_STYLE}" style follows your terminal' in result
