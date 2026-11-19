import pytest
from docstring_parser.google import parse
from docstring_parser.common import ParseError, Docstring, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_basic_google_style_docstring():
    docstring_text = """
    Short summary.

    Longer description that spans multiple lines.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If an error occurs.
    """
    result = parse(docstring_text)

    # Basic structure
    assert isinstance(result, Docstring)
    assert result.short_description == "Short summary."
    assert "Longer description" in result.long_description

    # Parameters
    assert len(result.params) == 2
    param1 = next(p for p in result.params if p.arg_name == "param1")
    assert isinstance(param1, DocstringParam)
    assert param1.type_name == "int"
    assert param1.description == "The first parameter."

    # Returns
    assert len(result.returns) == 1
    ret = result.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "bool"
    assert ret.description == "True if successful, False otherwise."

    # Raises
    assert len(result.raises) == 1
    raise_item = result.raises[0]
    assert isinstance(raise_item, DocstringRaises)
    assert raise_item.type_name == "ValueError"
    assert raise_item.description == "If an error occurs."

def test_parse_empty_and_none_input():
    # Empty string should produce an empty Docstring
    empty_result = parse("")
    assert isinstance(empty_result, Docstring)
    assert empty_result.short_description == ""
    assert empty_result.long_description == ""
    assert empty_result.params == []
    assert empty_result.returns == []
    assert empty_result.raises == []

    # None input should also produce an empty Docstring
    none_result = parse(None)
    assert isinstance(none_result, Docstring)
    assert none_result.short_description == ""
    assert none_result.long_description == ""
    assert none_result.params == []
    assert none_result.returns == []
    assert none_result.raises == []

def test_parse_invalid_section_raises_error():
    invalid_docstring = """
    Short summary.

    Args
        param1 (int): Missing colon after section header.
    """
    with pytest.raises(ParseError) as excinfo:
        parse(invalid_docstring)
    assert "Invalid section header" in str(excinfo.value)
