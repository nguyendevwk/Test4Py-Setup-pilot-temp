import pytest
from docstring_parser.numpydoc import parse
from docstring_parser.common import Docstring

def test_parse_numpydoc_parameters_and_none_input():
    doc = parse(
        "Summary.\n\nParameters\n----------\nx : int\n    Param x.\n"
    )
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Summary."
    assert len(doc.params) == 1
    param = doc.params[0]
    assert param.arg_name == "x"
    assert param.type_name == "int"
    assert param.description == "Param x."

    doc_none = parse(None)
    assert isinstance(doc_none, Docstring)
    assert doc_none.short_description is None
    assert doc_none.long_description == ""
    assert doc_none.params == []
