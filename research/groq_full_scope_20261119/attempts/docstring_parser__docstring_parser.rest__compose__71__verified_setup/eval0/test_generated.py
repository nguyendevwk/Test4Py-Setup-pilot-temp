import pytest
from docstring_parser.rest import compose
from docstring_parser.rest import RenderingStyle
from docstring_parser.rest import Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_compact_style_basic():
    doc = Docstring(
        short_description="Short",
        long_description="Long",
        meta=[
            DocstringParam(arg_name="x", type_name="int", description="the value"),
            DocstringReturns(type_name="int", description="result"),
            DocstringRaises(type_name="ValueError", description="if bad"),
        ],
    )
    result = compose(doc, RenderingStyle.COMPACT)
    expected = (
        "Short\n"
        "Long\n"
        ":param int x: the value\n"
        ":returns int: result\n"
        ":raises ValueError: if bad"
    )
    assert result == expected

def test_expanded_style_with_blank_lines():
    doc = Docstring(
        short_description="Start",
        blank_after_short_description=True,
        long_description="Middle",
        blank_after_long_description=True,
        meta=[
            DocstringParam(arg_name="y", description="y desc"),
            DocstringReturns(description="return desc"),
        ],
    )
    result = compose(doc, RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Start\n"
        "\n"
        "Middle\n"
        "\n"
        ":param y:\n"
        "  y desc\n"
        ":returns:\n"
        "  return desc"
    )
    assert result == expected

def test_clean_style_empty_descriptions():
    doc = Docstring(
        short_description="Only short",
        meta=[
            DocstringParam(arg_name="z", type_name="str", description=""),
            DocstringRaises(description=""),
        ],
    )
    result = compose(doc, RenderingStyle.CLEAN)
    expected = (
        "Only short\n"
        ":param str z:\n"
        ":raises :"
    )
    assert result == expected
