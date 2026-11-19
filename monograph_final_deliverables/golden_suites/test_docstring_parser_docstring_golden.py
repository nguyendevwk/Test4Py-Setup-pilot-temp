import pytest
from docstring_parser.common import Docstring, DocstringParam, Kind

def test_docstring_description_and_params_behavior():
    # Create a Docstring and set short and long descriptions
    doc = Docstring()
    doc.short_description = "Short summary."
    doc.blank_after_short_description = True
    doc.long_description = "Long description spanning multiple lines."
    # The description should concatenate short, blank line, and long
    expected = "Short summary.\n\nLong description spanning multiple lines."
    assert doc.description == expected

    # When no descriptions are set, description should be None
    doc.short_description = None
    doc.long_description = None
    assert doc.description is None

    # Add a normal param and an attribute param to meta
    param = DocstringParam(
        description="Param description",
        arg_name="x",
        type_name="int",
        is_optional=False,
        default=None,
        kind=Kind.PARAM,
    )
    attr = DocstringParam(
        description="Attribute description",
        arg_name="y",
        type_name="str",
        is_optional=True,
        default="'default'",
        kind=Kind.ATTRIBUTE,
    )
    doc.meta.extend([param, attr])

    # params should only include the non-attribute param
    assert len(doc.params) == 1
    assert doc.params[0].arg_name == "x"

    # attrs should only include the attribute param
    assert len(doc.attrs) == 1
    assert doc.attrs[0].arg_name == "y"

    # params_by_name should map the first occurrence of each name
    assert doc.params_by_name["x"] is doc.params[0]
    # attrs_by_name should map the first occurrence of each name
    assert doc.attrs_by_name["y"] is doc.attrs[0]
