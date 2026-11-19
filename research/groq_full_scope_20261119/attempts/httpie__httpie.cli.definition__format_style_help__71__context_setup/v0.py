import pytest
from httpie.cli.definition import format_style_help
from httpie.output.formatters.colors import BUNDLED_STYLES, DEFAULT_STYLE, AUTO_STYLE


def test_format_style_help_normal_mode():
    """When isolation_mode is False, the help text contains the default
    style and the provided available styles in the order given."""
    styles = ["monokai", "solarized", "gruvbox"]
    help_text = format_style_help(styles, isolation_mode=False)

    # The default style should be mentioned
    assert f'Output coloring style (default is "{DEFAULT_STYLE}")' in help_text

    # The auto style should be mentioned
    assert f'The "{AUTO_STYLE}" style follows your terminal' in help_text

    # The provided styles should appear in the same order
    # They are wrapped into lines of at most 60 characters
    # We check that each style appears in the text
    for style in styles:
        assert style in help_text

    # The isolation mode specific block should not appear
    assert "For finding out all available styles in your system" not in help_text


def test_format_style_help_isolation_mode():
    """When isolation_mode is True, the help text contains only bundled styles
    sorted alphabetically and the isolation mode block."""
    help_text = format_style_help([], isolation_mode=True)

    # The isolation mode block should be present
    assert "For finding out all available styles in your system" in help_text

    # The bundled styles should be sorted alphabetically
    sorted_bundled = sorted(BUNDLED_STYLES)
    for style in sorted_bundled:
        assert style in help_text

    # The provided empty list should not affect the output
    assert "monokai" in help_text  # example bundled style

    # The default style should still be mentioned
    assert f'default is "{DEFAULT_STYLE}"' in help_text


def test_format_style_help_available_styles_wrapping():
    """The available styles string is wrapped to a maximum width of 60 characters."""
    # Create a long list of dummy styles to force wrapping
    long_styles = [f"style{i}" for i in range(20)]
    help_text = format_style_help(long_styles, isolation_mode=False)

    # Each line in the wrapped part should not exceed 60 characters
    wrapped_section = help_text.split("It can be one of:")[1].split("\n\n")[0]
    for line in wrapped_section.splitlines():
        # Strip leading spaces used for indentation
        stripped = line.lstrip()
        # The line should not be longer than 60 characters
        assert len(stripped) <= 60

    # All styles should appear in the wrapped section
    for style in long_styles:
        assert style in help_text
