import pytest
from docstring_parser.rest import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns


def test_parse_basic_fields_and_meta():
    docstring = """Short description

:param name: param desc
:type name: str
:returns: return desc
"""
    doc = parse(docstring)

    # Basic Docstring object checks
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short description"
    assert doc.description.strip() == "Short description"

    # Meta entries
    assert len(doc.meta) == 3
    param_meta = next(m for m in doc.meta if isinstance(m, DocstringParam))
    returns_meta = next(m for m in doc.meta if isinstance(m, DocstringReturns))

    # Param meta checks
    assert param_meta.arg_name == "name"
    assert param_meta.description == "param desc"
    assert param_meta.type_name == "str"

    # Returns meta checks
    assert returns_meta.description == "return desc"

    # Convenience properties
    assert len(doc.params) == 1
    assert doc.params[0] is param_meta
    assert len(doc.returns) == 1
    assert doc.returns[0] is returns_meta

    # Parsing None yields an empty Docstring
    empty_doc = parse(None)
    assert isinstance(empty_doc, Docstring)
    assert empty_doc.meta == []
    assert empty_doc.description is None
