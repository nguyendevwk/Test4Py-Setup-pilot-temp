import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam


def test_parse_google_style_docstring_parses_params_and_description():
    text = """Short summary line.

Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.

Returns:
    bool: True if successful.
"""
    doc = parse(text)
    assert isinstance(doc, Docstring)

    # Short description is parsed correctly
    assert doc.short_description == "Short summary line."
    assert doc.description == "Short summary line."

    # No long description in this example
    assert doc.long_description is None

    # Two parameters parsed
    assert len(doc.params) == 2
    param1, param2 = doc.params
    assert isinstance(param1, DocstringParam)
    assert param1.arg_name == "param1"
    assert param1.type_name == "int"
    assert param1.description == "The first parameter."
    assert isinstance(param2, DocstringParam)
    assert param2.arg_name == "param2"
    assert param2.type_name == "str"
    assert param2.description == "The second parameter."

    # Mapping by name returns the first occurrence
    assert doc.params_by_name["param1"] is param1
    assert doc.params_by_name["param2"] is param2

    # No attributes or raises sections in this docstring
    assert doc.attrs == []
    assert doc.raises == []

    # Meta contains exactly the two parameters
    assert all(isinstance(m, DocstringParam) for m in doc.meta)
    assert set(m.arg_name for m in doc.meta) == {"param1", "param2"}

    # Parsing None yields an empty Docstring
    empty_doc = parse(None)
    assert isinstance(empty_doc, Docstring)
    assert empty_doc.description is None
    assert empty_doc.meta == []
