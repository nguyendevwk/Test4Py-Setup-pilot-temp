import pytest
from docstring_parser.rest import compose
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    RenderingStyle,
)

def test_compact_style_basic():
    """Test compact rendering with short and long description and a param."""
    doc = Docstring(
        short_description="Short",
        long_description="Long description",
        meta=[
            DocstringParam(
                arg_name="x",
                type_name="int",
                description="the value",
                is_optional=False,
            ),
            DocstringReturns(
                type_name="int",
                description="result",
                is_generator=False,
            ),
        ],
    )
    result = compose(doc, RenderingStyle.COMPACT)
    expected = (
        "Short\n"
        "Long description\n"
        ":param int x: the value\n"
        ":returns int: result"
    )
    assert result == expected

def test_expanded_style_with_blank_lines():
    """Test expanded rendering with blank lines after short and long descriptions."""
    doc = Docstring(
        short_description="Short",
        blank_after_short_description=True,
        long_description="Long description",
        blank_after_long_description=True,
        meta=[
            DocstringParam(
                arg_name="y",
                type_name=None,
                description="another value",
                is_optional=True,
            ),
            DocstringRaises(
                type_name="ValueError",
                description="if invalid",
            ),
        ],
    )
    result = compose(doc, RenderingStyle.EXPANDED)
    expected = (
        "Short\n"
        "\n"
        "Long description\n"
        "\n"
        ":param y:\n"
        " another value\n"
        ":raises ValueError : if invalid"
    )
    assert result == expected

def test_clean_style_description_formatting():
    """Test clean style ensures proper indentation of multi-line descriptions."""
    multi_line_desc = "First line\nSecond line\nThird line"
    doc = Docstring(
        short_description="Short",
        meta=[
            DocstringParam(
                arg_name="z",
                type_name="str",
                description=multi_line_desc,
                is_optional=False,
            ),
        ],
    )
    result = compose(doc, RenderingStyle.CLEAN, indent="  ")
    expected = (
        "Short\n"
        ":param str z: First line\n"
        "  Second line\n"
        "  Third line"
    )
    assert result == expected
