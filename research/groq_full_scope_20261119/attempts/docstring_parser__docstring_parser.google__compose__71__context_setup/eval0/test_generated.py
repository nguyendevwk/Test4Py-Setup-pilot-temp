import pytest
from docstring_parser.google import compose, RenderingStyle
from docstring_parser.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringMeta,
)

# Helper to build a minimal Docstring instance
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

def test_compose_compact_with_params_and_returns():
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
        description="True if successful",
        is_generator=False,
        args=("returns",),
    )
    doc = make_docstring(
        short_description="Adds two values.",
        params=params,
        returns=returns,
    )
    output = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")
    expected = (
        "Adds two values.\n"
        "Args:\n"
        "  x (int): the first value\n"
        "  y (str?): the second value\n"
        "Returns:\n"
        "  result (bool): True if successful"
    )
    assert output == expected

def test_compose_expanded_with_multiline_description_and_blank_lines():
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
        short_description="Process data.",
        long_description="This function processes data.\nIt is efficient.",
        params=params,
        blank_after_short_description=True,
        blank_after_long_description=True,
    )
    output = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Process data.\n"
        "\n"
        "This function processes data.\n"
        "It is efficient.\n"
        "\n"
        "Args:\n"
        "  data (list):\n"
        "    First line\n"
        "    Second line\n"
        "    Third line"
    )
    assert output == expected

def test_compose_invalid_rendering_style_raises_type_error():
    doc = make_docstring(short_description="Test.")
    with pytest.raises(TypeError):
        compose(doc, rendering_style="invalid_style")  # type: ignore[arg-type]
