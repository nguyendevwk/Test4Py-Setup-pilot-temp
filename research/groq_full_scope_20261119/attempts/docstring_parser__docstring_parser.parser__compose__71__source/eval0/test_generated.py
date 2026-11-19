import pytest
from docstring_parser import parser
from docstring_parser.common import Docstring, DocstringStyle, RenderingStyle


def test_compose_default_style_and_rendering():
    """Compose should use the docstring's own style when style is AUTO."""
    doc = Docstring(
        summary="Short summary",
        description="Detailed description.",
        style=DocstringStyle.GOOGLE,
        params=[],
        returns=None,
        raises=[],
        attributes=[],
        examples=[],
    )
    result = parser.compose(doc)
    # The output should start with the summary and include the description
    assert result.startswith("Short summary")
    assert "Detailed description." in result
    # Since the default rendering style is COMPACT, there should be no extra blank lines
    assert "\n\n" not in result.splitlines()[-2:]


def test_compose_override_style_google():
    """Compose should render using the specified style even if the docstring's style differs."""
    doc = Docstring(
        summary="Summary",
        description="Desc",
        style=DocstringStyle.REST,
        params=[],
        returns=None,
        raises=[],
        attributes=[],
        examples=[],
    )
    result = parser.compose(doc, style=DocstringStyle.GOOGLE)
    # Google style includes a blank line after the summary
    assert result.splitlines()[1] == ""
    # The description should follow the blank line
    assert result.splitlines()[2] == "Desc"


def test_compose_custom_indent():
    """Compose should respect the indent argument for nested blocks."""
    doc = Docstring(
        summary="S",
        description="D",
        style=DocstringStyle.NUMPYDOC,
        params=[
            parser.Param(
                name="x",
                type_name="int",
                description="x value",
                default=None,
                kind="positional",
            )
        ],
        returns=None,
        raises=[],
        attributes=[],
        examples=[],
    )
    result = parser.compose(doc, indent="  ")
    # In NumPy style, the parameter description is indented by 4 spaces by default.
    # With a custom indent of two spaces, the indentation should be two spaces.
    lines = result.splitlines()
    # Find the line that starts with "x : int"
    param_line = next(l for l in lines if l.lstrip().startswith("x :"))
    # The leading spaces should be exactly two
    assert param_line.startswith("  ")
