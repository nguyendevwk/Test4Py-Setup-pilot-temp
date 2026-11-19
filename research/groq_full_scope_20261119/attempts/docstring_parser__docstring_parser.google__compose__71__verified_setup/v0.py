import pytest
from docstring_parser.google import compose
from docstring_parser.google.common import (
    Docstring,
    DocstringParam,
    DocstringReturns,
    RenderingStyle,
)

# --------------------------------------------------------------------------- #
# Test 1: Compact rendering of a simple docstring with a required and an
# optional parameter, a return value and a raise clause.
# --------------------------------------------------------------------------- #
def test_compact_rendering_basic():
    doc = Docstring(
        short_description="Short",
        long_description="Long description.",
        params=[
            DocstringParam(
                arg_name="x",
                type_name="int",
                description="The first value.",
                is_optional=False,
                args=("param",),
            ),
            DocstringParam(
                arg_name="y",
                type_name="str",
                description="The second value.",
                is_optional=True,
                args=("param",),
            ),
        ],
        many_returns=[],
        returns=DocstringReturns(
            return_name="result",
            type_name="bool",
            description="True if successful.",
            args=("returns",),
        ),
        raises=[
            DocstringReturns(
                return_name="ValueError",
                type_name=None,
                description="If the input is invalid.",
                args=("raises",),
            )
        ],
        meta=[],
        blank_after_short_description=False,
        blank_after_long_description=False,
    )

    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")

    expected = (
        "Short\n"
        "Long description.\n"
        "Args:\n"
        "  x (int): The first value.\n"
        "  y (str?): The second value.\n"
        "Returns:\n"
        "  result (bool): True if successful.\n"
        "Raises:\n"
        "  ValueError: If the input is invalid."
    )
    assert rendered == expected


# --------------------------------------------------------------------------- #
# Test 2: Expanded rendering with multiline descriptions and a generator
# return. The generator should appear under "Yields:".
# --------------------------------------------------------------------------- #
def test_expanded_rendering_multiline_and_generator():
    doc = Docstring(
        short_description="Process data",
        long_description="This function processes data.\nIt yields results.",
        params=[
            DocstringParam(
                arg_name="data",
                type_name="Iterable[int]",
                description="An iterable of integers.\nEach integer is processed.",
                is_optional=False,
                args=("param",),
            ),
        ],
        many_returns=[
            DocstringReturns(
                return_name="item",
                type_name="int",
                description="A processed integer.\nMay be None.",
                is_generator=True,
                args=("returns",),
            )
        ],
        returns=None,
        raises=[],
        meta=[],
        blank_after_short_description=True,
        blank_after_long_description=True,
    )

    rendered = compose(doc, rendering_style=RenderingStyle.EXPANDED, indent="  ")

    expected = (
        "Process data\n"
        "\n"
        "This function processes data.\n"
        "It yields results.\n"
        "\n"
        "Args:\n"
        "  data (Iterable[int]):\n"
        "    An iterable of integers.\n"
        "    Each integer is processed.\n"
        "\n"
        "Yields:\n"
        "  item (int):\n"
        "    A processed integer.\n"
        "    May be None."
    )
    assert rendered == expected


# --------------------------------------------------------------------------- #
# Test 3: Handling of missing optional fields – when a parameter has no
# type_name and no description, the output should still contain the name
# and a colon.
# --------------------------------------------------------------------------- #
def test_missing_optional_fields():
    doc = Docstring(
        short_description="No type or description",
        params=[
            DocstringParam(
                arg_name="flag",
                type_name=None,
                description="",
                is_optional=False,
                args=("param",),
            ),
        ],
        many_returns=[],
        returns=None,
        raises=[],
        meta=[],
        blank_after_short_description=False,
        blank_after_long_description=False,
    )

    rendered = compose(doc, rendering_style=RenderingStyle.COMPACT, indent="  ")

    expected = (
        "No type or description\n"
        "Args:\n"
        "  flag:"
    )
    assert rendered == expected
