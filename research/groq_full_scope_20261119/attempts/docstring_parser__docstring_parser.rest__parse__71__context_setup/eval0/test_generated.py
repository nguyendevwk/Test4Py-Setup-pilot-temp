import pytest
from docstring_parser.rest import parse, ParseError
from docstring_parser.common import (
    DocstringParam,
    DocstringReturns,
    DocstringDeprecated,
    DocstringRaises,
)

def test_parse_basic_and_meta():
    doc = """
    Short description.

    Long description spanning
    multiple lines.

    :param int x: The first parameter.
    :param y: The second parameter, defaults to 10.
    :type z: str
    :rtype: bool
    :raises ValueError: If invalid.
    :deprecated 1.2.3 This will be removed.
    """
    result = parse(doc)

    # Short and long descriptions
    assert result.short_description == "Short description."
    assert result.long_description == "Long description spanning\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False

    # Meta items
    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 3
    x_param = next(p for p in params if p.arg_name == "x")
    assert x_param.type_name == "int"
    assert x_param.description == "The first parameter."
    y_param = next(p for p in params if p.arg_name == "y")
    assert y_param.type_name is None
    assert y_param.default == "10"
    z_param = next(p for p in params if p.arg_name == "z")
    assert z_param.type_name == "str"

    returns = [m for m in result.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    assert returns[0].type_name == "bool"

    raises = [m for m in result.meta if isinstance(m, DocstringRaises)]
    assert len(raises) == 1
    assert raises[0].type_name == "ValueError"

    deprecated = [m for m in result.meta if isinstance(m, DocstringDeprecated)]
    assert len(deprecated) == 1
    assert deprecated[0].version == "1.2.3"

def test_parse_boundary_empty_and_missing_meta():
    # Empty docstring
    assert parse("") == parse(None)

    # Docstring with only short description and no meta
    doc = "Only short description."
    result = parse(doc)
    assert result.short_description == "Only short description."
    assert result.long_description is None
    assert result.meta == []

    # Docstring with meta but no type/rtype specified
    doc = """
    :param a: first
    :param b: second
    """
    result = parse(doc)
    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 2
    for p in params:
        assert p.type_name is None

def test_parse_error_invalid_meta():
    # Meta line missing colon separator
    bad_doc = ":param int x The missing colon."
    with pytest.raises(ParseError) as excinfo:
        parse(bad_doc)
    assert 'Error parsing meta information' in str(excinfo.value)

    # Too many arguments for a param keyword
    bad_doc2 = ":param int x y z: too many"
    with pytest.raises(ParseError) as excinfo2:
        parse(bad_doc2)
    assert 'Expected one or two arguments' in str(excinfo2.value)
