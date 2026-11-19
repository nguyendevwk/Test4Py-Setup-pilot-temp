import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring


def test_parse_google_style_docstring_parses_params_and_description():
    text = '''Short summary line.

Args:
    param1 (int): The first parameter.
    param2 (str): The second parameter.

Returns:
    bool: True if successful.
'''
    doc = parse(text)

    # Verify the returned object type and basic description
    assert isinstance(doc, Docstring)
    assert doc.short_description == "Short summary line."
    assert doc.description.strip() == "Short summary line."

    # Verify that two parameters were parsed correctly
    assert len(doc.params) == 2
    p1, p2 = doc.params
    assert p1.arg_name == "param1"
    assert p1.type_name == "int"
    assert p1.description == "The first parameter."
    assert p2.arg_name == "param2"
    assert p2.type_name == "str"
    assert p2.description == "The second parameter."

    # Verify mapping by name and that no raises were parsed
    assert doc.params_by_name["param1"] is p1
    assert doc.params_by_name["param2"] is p2
    assert doc.raises == []
