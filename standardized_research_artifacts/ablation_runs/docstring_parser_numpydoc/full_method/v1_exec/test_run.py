import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring


def test_parse_numpydoc_parses_parameters_and_handles_none():
    # Normal numpy‑style docstring with a single parameter
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
    assert len(doc.params) == 1
    param = doc.params[0]
    assert param.arg_name == "param1"
    assert param.type_name == "int"
    assert param.description == "Desc."
    assert doc.attrs == []
    assert doc.raises == []

    # Parsing None should yield an empty Docstring
    doc_none = parse(None)
    assert isinstance(doc_none, Docstring)
    assert doc_none.description is None
