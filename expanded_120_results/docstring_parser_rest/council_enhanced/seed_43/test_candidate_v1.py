import pytest
from docstring_parser.rest import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, Kind


def test_parse_docstring_basic():
    doc = parse(":param name: param desc\n:type name: str\n:returns: return desc")
    assert isinstance(doc, Docstring)
    assert doc.short_description is None
    assert doc.long_description is None
    assert len(doc.meta) == 3

    param_meta = next(
        m for m in doc.meta if isinstance(m, DocstringParam) and m.arg_name == "name"
    )
    assert param_meta.description == "param desc"
    assert param_meta.type_name == "str"
    assert param_meta.kind is Kind.PARAM

    returns_meta = next(m for m in doc.meta if isinstance(m, DocstringReturns))
    assert returns_meta.description == "return desc"

    assert doc.params == [param_meta]
    assert doc.returns == [returns_meta]

    # None input yields an empty Docstring
    doc_none = parse(None)
    assert isinstance(doc_none, Docstring)
    assert doc_none.meta == []

    # Empty string input also yields an empty Docstring
    doc_empty = parse("")
    assert isinstance(doc_empty, Docstring)
    assert doc_empty.meta == []
