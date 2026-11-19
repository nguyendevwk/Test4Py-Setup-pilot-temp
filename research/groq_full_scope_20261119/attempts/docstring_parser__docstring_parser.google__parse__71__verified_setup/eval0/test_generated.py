import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, ParseError

def test_parse_simple_docstring():
    doc = """This function does something.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If x is negative.

    Examples:
        >>> result = my_func(1, 'a')
        >>> result
        True
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    # Description
    assert parsed.description.strip() == "This function does something."
    # Params
    assert len(parsed.params) == 2
    param_names = {p.arg_name for p in parsed.params}
    assert param_names == {"x", "y"}
    x_param = next(p for p in parsed.params if p.arg_name == "x")
    assert x_param.type_name == "int"
    assert x_param.description.strip() == "The first argument."
    # Returns
    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description.strip() == "True if successful, False otherwise."
    # Raises
    assert len(parsed.raises) == 1
    raise_item = parsed.raises[0]
    assert raise_item.type_name == "ValueError"
    assert raise_item.description.strip() == "If x is negative."
    # Examples
    assert len(parsed.examples) == 1
    example = parsed.examples[0]
    assert example.source.strip() == ">>> result = my_func(1, 'a')"
    assert example.expected_output.strip() == "True"

def test_parse_empty_docstring():
    parsed = parse("")
    assert isinstance(parsed, Docstring)
    assert parsed.description == ""
    assert parsed.params == []
    assert parsed.returns == []
    assert parsed.raises == []
    assert parsed.examples == []

def test_parse_invalid_docstring_raises_error():
    # Missing colon after Args section header
    bad_doc = """This function does something.

    Args
        x (int): The first argument.
    """
    with pytest.raises(ParseError):
        parse(bad_doc)
