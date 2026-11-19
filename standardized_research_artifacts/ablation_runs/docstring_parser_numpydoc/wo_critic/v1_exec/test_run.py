import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring, DocstringParam, Kind


def test_parse_basic_docstring():
    text = """Summary.

Parameters
----------
param1 : int
    Desc.
"""
    doc = parse(text)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Summary."
    assert doc.long_description is None
    assert doc.description == "Summary."
    assert len(doc.meta) == 1
    param = doc.meta[0]
    assert isinstance(param, DocstringParam)
    assert param.arg_name == "param1"
    assert param.type_name == "int"
    assert param.description == "Desc."
    # Kind may be named PARAMETER or PARAM; accept either
    assert param.kind is not None
    assert param.kind in (getattr(Kind, "PARAMETER", None), getattr(Kind, "PARAM", None))
    assert doc.params == [param]
    assert doc.attrs == []
    assert doc.raises == []

    # Parsing None should yield an empty Docstring
    empty_doc = parse(None)
    assert isinstance(empty_doc, Docstring)
    assert empty_doc.short_description is None
    assert empty_doc.long_description is None
    assert empty_doc.description is None
    assert empty_doc.meta == []
