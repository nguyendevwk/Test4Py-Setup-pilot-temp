import pytest
from docstring_parser.rest import parse
from docstring_parser.common import (
    DocstringParam,
    DocstringReturns,
    DocstringMeta,
    ParseError,
)

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

    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 1
    param = params[0]
    assert param.arg_name == "a"
    assert param.description == "description of a"
    assert param.type_name == "int"

    returns = [m for m in result.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    ret = returns[0]
    assert ret.return_name is None
    assert ret.description == "result"
    assert ret.type_name == "str"

def test_parse_missing_meta_and_blank_lines():
    doc = """
    Only short description.

    :param b: param without type
    :raises ValueError: if something
    """
    result = parse(doc)
    assert result.short_description == "Only short description."
    assert result.long_description is None
    assert result.blank_after_short_description is False

    meta = result.meta
    assert any(isinstance(m, DocstringMeta) and m.args == ["raises", "ValueError"] for m in meta)
    assert any(isinstance(m, DocstringMeta) and m.args == ["param", "b"] for m in meta)

def test_parse_invalid_meta_raises_error():
    doc = """
    :param: missing argument name
    """
    with pytest.raises(ParseError) as excinfo:
        parse(doc)
    assert 'Error parsing meta information' in str(excinfo.value)
