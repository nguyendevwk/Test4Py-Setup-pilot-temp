import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import DocstringStyle


def test_parse_basic_docstring_and_none():
    docstring = """Summary.

Long description.

Parameters
----------
param1 : int
    First param.
param2 : str
    Second param.

Returns
-------
int
    Result.
"""
    doc = parse(docstring)

    # Style and description
    assert doc.style is DocstringStyle.NUMPY
    assert doc.short_description == "Summary."
    assert doc.long_description == "Long description."
    assert doc.blank_after_short_description is True
    assert doc.description == "Summary.\n\nLong description."

    # Parameters
    assert len(doc.params) == 2
    assert [p.arg_name for p in doc.params] == ["param1", "param2"]

    # None input yields empty Docstring
    empty_doc = parse(None)
    assert empty_doc.short_description is None
    assert empty_doc.long_description is None
    assert empty_doc.params == []
