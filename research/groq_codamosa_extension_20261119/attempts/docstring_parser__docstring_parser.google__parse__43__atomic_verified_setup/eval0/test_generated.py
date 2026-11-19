import pytest
from docstring_parser.google import parse
from docstring_parser.common import ParseError, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_normal_docstring():
    doc = """
    Calculates the sum of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.

    Raises:
        ValueError: If either argument is not an integer.

    Examples:
        >>> add(2, 3)
        5
    """
    result = parse(doc)
    # Basic description
    assert result.description.strip() == "Calculates the sum of two numbers."
    # Parameters
    assert len(result.params) == 2
    a_param = next(p for p in result.params if p.arg_name == "a")
    assert isinstance(a_param, DocstringParam)
    assert a_param.type_name == "int"
    assert a_param.description == "The first number."
    # Returns
    assert len(result.returns) == 1
    ret = result.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "int"
    assert ret.description == "The sum of a and b."
    # Raises
    assert len(result.raises) == 1
    raise_item = result.raises[0]
    assert isinstance(raise_item, DocstringRaises)
    assert raise_item.type_name == "ValueError"
    assert raise_item.description == "If either argument is not an integer."
    # Examples
    assert len(result.examples) == 1
    assert result.examples[0].code.strip() == ">>> add(2, 3)"
    assert result.examples[0].output.strip() == "5"

def test_parse_empty_docstring():
    # Empty string should produce a Docstring with empty fields
    result = parse("")
    assert result.description == ""
    assert result.params == []
    assert result.returns == []
    assert result.raises == []
    assert result.examples == []

def test_parse_invalid_docstring_raises_error():
    # Malformed section header should raise ParseError
    bad_doc = """
    This is a docstring with an invalid section.

    BadSection
        Something
    """
    with pytest.raises(ParseError):
        parse(bad_doc)
