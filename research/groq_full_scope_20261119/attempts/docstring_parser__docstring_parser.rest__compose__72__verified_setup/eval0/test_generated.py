import pytest
from docstring_parser.rest import compose, RenderingStyle
from docstring_parser.rest.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringMeta,
)

# Helper to create a minimal Docstring instance
def make_docstring(
    short_description="",
    blank_after_short_description=False,
    long_description="",
    blank_after_long_description=False,
    meta=None,
):
    return Docstring(
        short_description=short_description,
        blank_after_short_description=blank_after_short_description,
        long_description=long_description,
        blank_after_long_description=blank_after_long_description,
        meta=meta or [],
    )

def test_compose_basic_short_and_long():
    """Test rendering of short and long descriptions with a simple param."""
    doc = make_docstring(
        short_description="Short",
        long_description="Long description.",
        meta=[
            DocstringParam(
                arg_name="x",
                description="an integer",
                type_name="int",
                is_optional=False,
            )
        ],
    )
    result = compose(doc, RenderingStyle.COMPACT)
    expected = (
        "Short\n"
        "Long description.\n"
        ":param int x: an integer"
    )
    assert result == expected

def test_compose_boundary_empty_descriptions_and_optional_type():
    """Test rendering when descriptions are empty and the param is optional."""
    doc = make_docstring(
        short_description="",
        meta=[
            DocstringParam(
                arg_name="y",
                description="",
                type_name="str",
                is_optional=True,
            ),
            DocstringReturns(
                description="",
                type_name="bool",
                is_generator=False,
            ),
            DocstringRaises(
                description="",
                type_name="ValueError",
            ),
        ],
    )
    result = compose(doc, RenderingStyle.COMPACT)
    # Empty descriptions should not add trailing spaces
    expected = (
        ":param str? y:\n"
        ":returns bool:\n"
        ":raises ValueError :"
    )
    assert result == expected

def test_compose_expanded_style_with_multiline_description():
    """Test rendering with EXPANDED style and multiline descriptions."""
    long_desc = "First line\nSecond line"
    param_desc = "Param line 1\nParam line 2"
    doc = make_docstring(
        short_description="Header",
        blank_after_short_description=True,
        long_description=long_desc,
        meta=[
            DocstringParam(
                arg_name="z",
                description=param_desc,
                type_name="float",
                is_optional=False,
            )
        ],
    )
    result = compose(doc, RenderingStyle.EXPANDED, indent="  ")
    expected = (
        "Header\n\n"
        "First line\n"
        "Second line\n\n"
        ":param z:\n"
        "  Param line 1\n"
        "  Param line 2\n"
        ":type z: float"
    )
    assert result == expected
