import pytest
from docstring_parser.rest import parse, ParseError
from docstring_parser.common import (
    DocstringParam,
    DocstringReturns,
    DocstringDeprecated,
    DocstringRaises,
)

def test_parse_basic_and_type_inference():
    doc = """
    Short description.

    Long description spanning
    multiple lines.

    :param int x: the first value
    :param y: the second value defaults to 10
    :type z: str
    :rtype: bool
    """
    result = parse(doc)

    # Short and long descriptions
    assert result.short_description == "Short description."
    assert result.long_description == "Long description spanning\nmultiple lines."
    assert result.blank_after_short_description is False
    assert result.blank_after_long_description is False

    # Parameters
    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 2
    x_param = next(p for p in params if p.arg_name == "x")
    y_param = next(p for p in params if p.arg_name == "y")
    assert x_param.type_name == "int"
    assert x_param.is_optional is None
    assert x_param.default is None
    assert y_param.type_name is None
    assert y_param.default == "10"

    # Type inference from :type
    z_param = next(p for p in params if p.arg_name == "z")
    assert z_param.type_name == "str"

    # Return type inference
    returns = [m for m in result.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    assert returns[0].type_name == "bool"
    assert returns[0].return_name is None

def test_parse_deprecation_and_raises():
    doc = """
    :deprecated v2.0 This feature is obsolete.
    :raises ValueError: if the value is negative
    :raises: generic exception
    """
    result = parse(doc)

    # Deprecation
    deprecations = [m for m in result.meta if isinstance(m, DocstringDeprecated)]
    assert len(deprecations) == 1
    dep = deprecations[0]
    assert dep.version == "v2.0"
    assert dep.description == "This feature is obsolete."

    # Raises
    raises = [m for m in result.meta if isinstance(m, DocstringRaises)]
    assert len(raises) == 2
    val_err = next(r for r in raises if r.type_name == "ValueError")
    generic = next(r for r in raises if r.type_name is None)
    assert val_err.description == "if the value is negative"
    assert generic.description == "generic exception"

def test_parse_invalid_meta_raises_error():
    # Missing colon after key
    bad_doc = ":param int x this is wrong"
    with pytest.raises(ParseError) as excinfo:
        parse(bad_doc)
    assert 'Error parsing meta information' in str(excinfo.value)

    # Too many arguments for :param
    bad_doc2 = ":param int x y z: too many"
    with pytest.raises(ParseError) as excinfo2:
        parse(bad_doc2)
    assert 'Expected one or two arguments for a param keyword' in str(excinfo2.value)
