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
    param = DocstringParam(
        arg_name="x",
        type_name="int",
        description="The input value",
        is_optional=False,
    )
    returns = DocstringReturns(
        type_name="int",
        description="The result",
        is_generator=False,
    )
    doc = Docstring(
        short_description="Compute",
        meta=[param, returns],
        blank_after_short_description=False,
        blank_after_long_description=False,
    )
    result = compose(doc, RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Compute\n"
        "\n  :param x:\n  The input value\n"
        "  :type x: int\n"
        "\n  :returns:\n  The result\n"
        "  :rtype: int"
    )
    assert result == expected

def test_compose_with_raises_and_clean_style():
    raises = DocstringRaises(
        type_name="ValueError",
        description="If input is invalid",
    )
    meta = DocstringMeta(args=("custom",), description="Custom meta")
    doc = Docstring(
        short_description="Check",
        meta=[raises, meta],
        blank_after_short_description=False,
        blank_after_long_description=False,
    )
    result = compose(doc, RenderingStyle.CLEAN, indent="  ")
    expected = (
        "Check\n"
        ":raises ValueError :If input is invalid\n"
        ":custom :Custom meta"
    )
    assert result == expected
