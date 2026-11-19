import pytest
from docstring_parser.google import parse
from docstring_parser.common import ParseError, Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_normal_docstring():
    doc = """
    Short summary.

    Longer description that spans
    multiple lines.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful.

    Raises:
        ValueError: If the input is invalid.
    """
    result = parse(doc)
    assert isinstance(result, Docstring)
    # Summary and description
    assert result.short_description == "Short summary."
    assert "Longer description" in result.long_description
    # Parameters
    assert len(result.params) == 2
    param_x = next(p for p in result.params if p.arg_name == "x")
    assert param_x.type_name == "int"
    assert param_x.description == "The first argument."
    param_y = next(p for p in result.params if p.arg_name == "y")
    assert param_y.type_name == "str"
    # Returns
    assert len(result.returns) == 1
    ret = result.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description == "True if successful."
    # Raises
    assert len(result.raises) == 1
    r = result.raises[0]
    assert isinstance(r, DocstringRaises)
    assert r.type_name == "ValueError"
    assert r.description == "If the input is invalid."

def test_parse_empty_docstring():
    result = parse("")
    assert isinstance(result, Docstring)
    assert result.short_description == ""
    assert result.long_description == ""
    assert result.params == []
    assert result.returns == []
    assert result.raises == []

def test_parse_invalid_section():
    bad_doc = """
    Summary.

    Args:
        x (int) The missing colon.
    """
    with pytest.raises(ParseError):
        parse(bad_doc)
