import pytest
from docstring_parser.google import compose
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    RenderingStyle,
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

def test_compose_basic_compact_style():
    """Test that a simple docstring with one param and a return is rendered correctly in compact style."""
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
        description="The result.",
        args=("returns",),
    )
    doc = make_docstring(
        short_description="Adds two numbers.",
        params=[param],
        returns=ret,
    )
    result = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Adds two numbers.\n"
        "Args:\n"
        "  x (int): The input value.\n"
        "\n"
        "Returns:\n"
        "  result (int): The result."
    )
    assert result == expected

def test_compose_expanded_style_with_optional_and_generator():
    """Test expanded style rendering with an optional parameter and a generator return."""
    param = DocstringParam(
        arg_name="y",
        type_name="str",
        description="Optional name.\nMay be empty.",
        is_optional=True,
        args=("param",),
    )
    gen_ret = DocstringReturns(
        return_name="values",
        type_name="int",
        description="Yielded values.",
        is_generator=True,
        args=("returns",),
    )
    doc = make_docstring(
        short_description="Iterates over values.",
        long_description="This function yields values.",
        params=[param],
        many_returns=[gen_ret],
        blank_after_short_description=True,
        blank_after_long_description=True,
    )
    result = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Iterates over values.\n"
        "\n"
        "This function yields values.\n"
        "\n"
        "Args:\n"
        "  y (str, optional):\n"
        "    Optional name.\n"
        "    May be empty.\n"
        "\n"
        "Yields:\n"
        "  values (int):\n"
        "    Yielded values."
    )
    assert result == expected

def test_compose_with_raises_and_meta():
    """Test that raises and meta sections are rendered correctly."""
    raise_item = DocstringRaises(
        type_name="ValueError",
        description="If the input is invalid.",
        args=("raises",),
    )
    meta_item = DocstringMeta(
        args=("author",),
        description="John Doe",
    )
    doc = make_docstring(
        short_description="Raises error on bad input.",
        raises=[raise_item],
        meta=[meta_item],
    )
    result = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Raises error on bad input.\n"
        "Raises:\n"
        "  ValueError: If the input is invalid.\n"
        "\n"
        "Author:\n"
        "  John Doe\n"
    )
    assert result == expected
