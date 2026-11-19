import pytest
from docstring_parser.rest import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, Kind


def test_parse_rest_docstring_parses_sections_and_meta():
    # Arrange: a minimal ReST docstring with param, type, and returns
    docstring_text = ":param name: param desc\n:type name: str\n:returns: return desc"

    # Act: parse the docstring
    doc = parse(docstring_text)

    # Assert: the result is a Docstring instance
    assert isinstance(doc, Docstring)

    # The meta list should contain two entries: param and returns
    assert len(doc.meta) == 2

    # First meta: a DocstringParam for the parameter
    param_meta = doc.meta[0]
    assert isinstance(param_meta, DocstringParam)
    assert param_meta.arg_name == "name"
    assert param_meta.kind is Kind.PARAM
    assert param_meta.description == "param desc"
    assert param_meta.type_name == "str"

    # Second meta: a DocstringReturns for the return description
    returns_meta = doc.meta[1]
    assert isinstance(returns_meta, DocstringReturns)
    assert returns_meta.description == "return desc"

    # The convenience properties should expose the expected items
    assert doc.params == [param_meta]
    assert doc.attrs == []
    assert doc.params_by_name == {"name": param_meta}
    assert doc.attrs_by_name == {}

    # No short or long description was provided, so description should be None
    assert doc.description is None

    # Parsing an empty docstring yields an empty Docstring
    empty_doc = parse("")
    assert isinstance(empty_doc, Docstring)
    assert empty_doc.meta == []
    assert empty_doc.description is None
