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
    """Test rendering of a simple docstring with compact style."""
    doc = Docstring(
        short_description="Short",
        long_description="Long description",
        meta=[
            DocstringParam(arg_name="x", type_name="int", description="the value"),
            DocstringReturns(type_name="int", description="the result"),
            DocstringRaises(type_name="ValueError", description="if invalid"),
        ],
    )
    result = compose(doc, rendering_style=RenderingStyle.COMPACT)
    expected = (
        "Short\n"
        "Long description\n"
        ":param int x: the value\n"
        ":returns int: the result\n"
        ":raises ValueError: if invalid"
    )
    assert result == expected

def test_expanded_style_with_optional_and_blank():
    """Test expanded style with optional type and blank lines."""
    doc = Docstring(
        short_description="Compute",
        blank_after_short_description=True,
        long_description="Performs computation.",
        blank_after_long_description=True,
        meta=[
            DocstringParam(
                arg_name="data",
                type_name="list",
                is_optional=True,
                description="Input data",
            ),
            DocstringReturns(
                type_name="float",
                is_generator=False,
                description="Result value",
            ),
        ],
    )
    result = compose(doc, rendering_style=RenderingStyle.EXPANDED)
    expected = (
        "Compute\n"
        "\n"
        "Performs computation.\n"
        "\n"
        ":param data:\n"
        " Input data\n"
        ":type data: list?\n"
        ":returns:\n"
        " Result value\n"
        ":rtype: float"
    )
    assert result == expected

def test_clean_style_no_descriptions():
    """Test clean style when descriptions are missing."""
    doc = Docstring(
        short_description="NoDesc",
        meta=[
            DocstringParam(arg_name="a", type_name="str"),
            DocstringRaises(type_name="KeyError"),
        ],
    )
    result = compose(doc, rendering_style=RenderingStyle.CLEAN)
    expected = (
        "NoDesc\n"
        ":param str a:\n"
        ":raises KeyError:"
    )
    assert result == expected
