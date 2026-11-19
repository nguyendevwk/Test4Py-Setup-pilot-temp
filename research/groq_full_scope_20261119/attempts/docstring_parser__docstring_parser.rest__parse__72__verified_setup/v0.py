import pytest
from docstring_parser.rest import parse
from docstring_parser.common import ParseError, DocstringParam, DocstringReturns

def test_parse_basic_docstring():
    doc = """
    Short description.

    Long description spanning
    multiple lines.

    :param a: description of a
    :type a: int
    :return: result
    :rtype: str
    """
    result = parse(doc)
    assert result.style.name == "REST"
    assert result.short_description == "Short description."
    assert result.long_description == "Long description spanning\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False
    assert len(result.meta) == 2
    param = next(m for m in result.meta if isinstance(m, DocstringParam))
    assert param.arg_name == "a"
    assert param.description == "description of a"
    assert param.type_name == "int"
    ret = next(m for m in result.meta if isinstance(m, DocstringReturns))
    assert ret.return_name is None
    assert ret.description == "result"
    assert ret.type_name == "str"

def test_parse_empty_and_missing_meta():
    # Empty docstring should return an empty Docstring object
    empty = parse("")
    assert empty.short_description is None
    assert empty.long_description is None
    assert empty.meta == []

    # Docstring with no meta tags
    doc = "Only a short description."
    result = parse(doc)
    assert result.short_description == "Only a short description."
    assert result.long_description is None
    assert result.meta == []

def test_parse_invalid_meta_raises_error():
    # Meta section missing a colon after the key
    bad_doc = """
    :param a description of a
    """
    with pytest.raises(ParseError) as excinfo:
        parse(bad_doc)
    assert 'Error parsing meta information near' in str(excinfo.value)
