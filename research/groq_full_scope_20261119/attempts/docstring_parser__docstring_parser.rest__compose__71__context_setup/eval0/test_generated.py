import pytest
from docstring_parser.rest import compose, RenderingStyle
from docstring_parser.rest.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringMeta,
)

def test_compose_basic_short_and_long_description():
    doc = Docstring(
        short_description="Short",
        long_description="Long description line 1\nLong description line 2",
        blank_after_short_description=False,
        blank_after_long_description=False,
        meta=[],
    )
    result = compose(doc, RenderingStyle.COMPACT)
    expected = (
        "Short\n"
        "Long description line 1\n"
        "Long description line 2"
    )
    assert result == expected

def test_compose_with_params_and_returns_expanded():
    doc = Docstring(
        short_description="",
        long_description="",
        blank_after_short_description=False,
        blank_after_long_description=False,
        meta=[
            DocstringParam(arg_name="x", type_name="int", is_optional=False, description="an integer"),
            DocstringReturns(type_name="str", description="a string", is_generator=False),
        ],
    )
    result = compose(doc, RenderingStyle.EXPANDED)
    expected = (
        "\n    :param x:\n    an integer\n"
        ":type x: int\n"
        "\n    :returns:\n    a string\n"
        ":rtype: str"
    )
    assert result == expected

def test_compose_with_raises_and_custom_meta():
    custom_meta = DocstringMeta(args=("custom",), description="custom meta")
    doc = Docstring(
        short_description="",
        long_description="",
        blank_after_short_description=False,
        blank_after_long_description=False,
        meta=[
            DocstringRaises(type_name="ValueError", description="invalid value"),
            custom_meta,
        ],
    )
    result = compose(doc, RenderingStyle.CLEAN)
    expected = (
        ":raises ValueError :invalid value\n"
        ":custom: custom meta"
    )
    assert result == expected
