import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises, DocstringExample

def test_parse_simple_google_docstring():
    doc = """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of a and b.

    Raises:
        ValueError: If either argument is negative.

    Examples:
        >>> add(2, 3)
        5
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    assert parsed.description.strip() == "Adds two numbers together."
    assert len(parsed.params) == 2
    names = {p.name for p in parsed.params}
    assert names == {"a", "b"}
    for p in parsed.params:
        assert isinstance(p, DocstringParam)
        assert p.type_name == "int"
    assert len(parsed.returns) == 1
    ret = parsed.returns[0]
    assert isinstance(ret, DocstringReturns)
    assert ret.type_name == "int"
    assert ret.description == "The sum of a and b."
    assert len(parsed.raises) == 1
    r = parsed.raises[0]
    assert isinstance(r, DocstringRaises)
    assert r.type_name == "ValueError"
    assert r.description == "If either argument is negative."
    assert len(parsed.examples) == 1
    ex = parsed.examples[0]
    assert isinstance(ex, DocstringExample)
    assert ex.code.strip() == ">>> add(2, 3)"
    assert ex.expected_output.strip() == "5"

def test_parse_empty_docstring_returns_empty_docstring():
    parsed = parse("")
    assert isinstance(parsed, Docstring)
    assert parsed.description == ""
    assert parsed.params == []
    assert parsed.returns == []
    assert parsed.raises == []
    assert parsed.examples == []

def test_parse_invalid_input_raises_type_error():
    with pytest.raises(TypeError):
        parse(42)  # non-string input should raise TypeError
