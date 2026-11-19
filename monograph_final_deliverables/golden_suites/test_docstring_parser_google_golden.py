import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns

def test_parse_google_style_docstring():
    text = '''Short summary line.

Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.

Returns:
    bool: True if successful.
'''
    doc = parse(text)
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary line."
    assert doc.long_description is None
    assert len(doc.params) == 2
    param1, param2 = doc.params
    assert isinstance(param1, DocstringParam)
    assert param1.arg_name == "param1"
    assert param1.type_name == "int"
    assert param1.description == "The first parameter."
    assert param2.arg_name == "param2"
    assert param2.type_name == "str"
    assert param2.description == "The second parameter."
    returns = [m for m in doc.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    ret = returns[0]
    assert ret.type_name == "bool"
    assert ret.description == "True if successful."
    # test parsing None
    none_doc = parse(None)
    assert isinstance(none_doc, Docstring)
    assert none_doc.short_description is None
    assert none_doc.long_description is None
    assert none_doc.meta == []
