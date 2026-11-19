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
        description="If the input is negative.",
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
        "  ValueError: If the input is negative."
    )
    assert rendered == expected

def test_compose_expanded_style_with_optional_and_multiline(tmp_path):
    # Optional param with multiline description and generator return
    param = DocstringParam(
        arg_name="y",
        type_name="str",
        description="First line.\nSecond line.",
        is_optional=True,
        args=("param",),
    )
    ret = DocstringReturns(
        return_name="items",
        type_name="Iterator[str]",
        description="Yielded items.\nEach item is a string.",
        is_generator=True,
        args=("returns",),
    )
    doc = make_docstring(
        short_description="Yield items.",
        long_description="This function yields items lazily.",
        params=[param],
        many_returns=[ret],
        blank_after_short_description=True,
        blank_after_long_description=True,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Yield items.\n"
        "\n"
        "This function yields items lazily.\n"
        "\n"
        "Args:\n"
        "  y (str, optional):\n"
        "    First line.\n"
        "    Second line.\n"
        "\n"
        "Yields:\n"
        "  items (Iterator[str]):\n"
        "    Yielded items.\n"
        "    Each item is a string."
    )
    assert rendered == expected

def test_compose_meta_and_blank_lines(tmp_path):
    # Test that meta sections are rendered and trailing blanks are trimmed
    meta = DocstringMeta(
        args=("author",),
        description="John Doe",
    )
    doc = make_docstring(
        short_description="Meta test.",
        meta=[meta],
        blank_after_short_description=True,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Meta test.\n"
        "\n"
        "Author:\n"
        "  John Doe\n"
    )
    assert rendered == expected
