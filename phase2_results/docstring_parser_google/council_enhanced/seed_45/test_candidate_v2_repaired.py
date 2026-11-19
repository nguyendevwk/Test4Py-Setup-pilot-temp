import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringReturns

def test_parse_google_style_docstring_parses_sections_and_metadata():
    text = """Short summary line.

This is a long description that spans
multiple lines.

Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.

Returns:
    bool: True if successful.
"""
    doc = parse(text)

    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary line."
    assert doc.long_description == "This is a long description that spans\nmultiple lines."
    assert doc.blank_after_short_description is True
    assert doc.blank_after_long_description is True

    expected_description = "Short summary line.\n\nThis is a long description that spans\nmultiple lines."
    assert doc.description == expected_description

    assert len(doc.params) == 2
    param_names = {p.arg_name for p in doc.params}
    assert param_names == {"param1", "param2"}
    assert doc.params_by_name["param1"].arg_name == "param1"
    assert doc.params_by_name["param2"].arg_name == "param2"

    assert isinstance(doc.returns, DocstringReturns)
    ret = doc.returns
    assert ret.type_name == "bool"
    assert ret.description == "True if successful."

    empty_doc = parse(None)
    assert isinstance(empty_doc, Docstring)
    assert empty_doc.meta == []
    assert empty_doc.short_description is None
    assert empty_doc.long_description is None
