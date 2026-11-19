import pytest
from docstring_parser.google import compose, RenderingStyle
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringMeta,
)

# Helper to create a minimal Docstring instance
def make_docstring(
    short_description="",
    long_description="",
    params=None,
    many_returns=None,
    returns=None,
    raises=None,
    meta=None,
    blank_after_short_description=False,
    blank_after_long_description=False,
):
    return Docstring(
        short_description=short_description,
        long_description=long_description,
        params=params or [],
        many_returns=many_returns or [],
        returns=returns,
        raises=raises or [],
        meta=meta or [],
        blank_after_short_description=blank_after_short_description,
        blank_after_long_description=blank_after_long_description,
    )

def test_compose_basic_compact_style(tmp_path):
    # Create a simple docstring with one param, one return, and one raise
    param = DocstringParam(
        arg_name="x",
        type_name="int",
        description="The input value.",
        is_optional=False,
        args=("param",),
    )
    ret = DocstringReturns(
        return_name="result",
        type_name="int",
        description="The computed result.",
        args=("returns",),
    )
    raise_exc = DocstringRaises(
        type_name="ValueError",
        description="If x is negative.",
        args=("raises",),
    )
    doc = make_docstring(
        short_description="Compute something.",
        params=[param],
        returns=ret,
        raises=[raise_exc],
    )
    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Compute something.\n"
        "Args:\n"
        "  x (int): The input value.\n"
        "\n"
        "Returns:\n"
        "  result (int): The computed result.\n"
        "\n"
        "Raises:\n"
        "  ValueError: If x is negative."
    )
    assert rendered == expected

def test_compose_expanded_style_with_optional_and_blank(tmp_path):
    # Optional param, expanded style, blank lines after sections
    param = DocstringParam(
        arg_name="y",
        type_name="str",
        description="An optional string.\nIt can span multiple lines.",
        is_optional=True,
        args=("param",),
    )
    doc = make_docstring(
        short_description="Process data.",
        long_description="This function processes data.\nIt is robust.",
        params=[param],
        blank_after_short_description=True,
        blank_after_long_description=True,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Process data.\n"
        "\n"
        "This function processes data.\n"
        "It is robust.\n"
        "\n"
        "Args:\n"
        "  y (str, optional):\n"
        "    An optional string.\n"
        "    It can span multiple lines."
    )
    assert rendered == expected

def test_compose_meta_and_many_returns(tmp_path):
    # Test handling of many_returns and meta sections
    ret1 = DocstringReturns(
        return_name="a",
        type_name="int",
        description="First value.",
        args=("returns",),
    )
    ret2 = DocstringReturns(
        return_name="b",
        type_name="int",
        description="Second value.",
        is_generator=True,
        args=("returns",),
    )
    meta = DocstringMeta(
        args=("author",),
        description="John Doe",
    )
    doc = make_docstring(
        short_description="Return multiple values.",
        many_returns=[ret1, ret2],
        meta=[meta],
    )
    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Return multiple values.\n"
        "Returns:\n"
        "  a (int): First value.\n"
        "\n"
        "Yields:\n"
        "  b (int): Second value.\n"
        "\n"
        "Author:\n"
        "  John Doe"
    )
    assert rendered == expected
