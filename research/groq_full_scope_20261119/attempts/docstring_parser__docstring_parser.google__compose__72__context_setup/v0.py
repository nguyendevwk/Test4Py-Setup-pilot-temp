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

def test_compose_basic_compact():
    """Test compact rendering of a simple docstring with params and returns."""
    params = [
        DocstringParam(
            arg_name="x",
            type_name="int",
            description="the first value",
            is_optional=False,
            args=("param",),
        ),
        DocstringParam(
            arg_name="y",
            type_name="str",
            description="the second value",
            is_optional=True,
            args=("param",),
        ),
    ]
    returns = DocstringReturns(
        return_name="result",
        type_name="bool",
        description="whether successful",
        args=("returns",),
    )
    doc = make_docstring(
        short_description="Compute something",
        params=params,
        returns=returns,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Compute something\n"
        "Args:\n"
        "  x (int): the first value\n"
        "  y (str?): the second value\n"
        "Returns:\n"
        "  result (bool): whether successful"
    )
    assert rendered == expected

def test_compose_expanded_multiline_description():
    """Test expanded rendering with multiline descriptions and blank lines."""
    params = [
        DocstringParam(
            arg_name="data",
            type_name="list",
            description="First line\nSecond line\nThird line",
            is_optional=False,
            args=("param",),
        ),
    ]
    doc = make_docstring(
        short_description="Process data",
        blank_after_short_description=True,
        long_description="This function processes data.\nIt is efficient.",
        blank_after_long_description=True,
        params=params,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Process data\n\n"
        "This function processes data.\nIt is efficient.\n\n"
        "Args:\n"
        "  data (list):\n"
        "    First line\n"
        "    Second line\n"
        "    Third line"
    )
    assert rendered == expected

def test_compose_meta_and_raises():
    """Test handling of meta tags and raises section."""
    raises = [
        DocstringRaises(
            type_name="ValueError",
            description="if input is invalid",
            args=("raises",),
        )
    ]
    meta = [
        DocstringMeta(
            args=("author",),
            description="John Doe",
        ),
        DocstringMeta(
            args=("version",),
            description="1.0.0",
        ),
    ]
    doc = make_docstring(
        short_description="Validate input",
        params=[],
        raises=raises,
        meta=meta,
    )
    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Validate input\n"
        "Raises:\n"
        "  ValueError: if input is invalid\n"
        "Author:\n"
        "  John Doe\n"
        "Version:\n"
        "  1.0.0"
    )
    assert rendered == expected
