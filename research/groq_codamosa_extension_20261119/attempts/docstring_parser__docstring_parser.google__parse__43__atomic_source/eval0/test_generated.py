import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, ParseError

def test_parse_normal_docstring():
    doc = """
    This function does something.

    Args:
        x (int): The first argument.
        y (str): The second argument.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If x is negative.
        TypeError: If y is not a string.

    Examples:
        >>> result = my_func(1, "test")
        >>> result
        True
    """
    parsed = parse(doc)
    assert isinstance(parsed, Docstring)
    # Parameters
    assert len(parsed.params) == 2
    param_names = {p.arg_name for p in parsed.params}
    assert param_names == {"x", "y"}
    # Return
    assert parsed.returns is not None
    assert parsed.returns.type_name == "bool"
    # Raises
    assert len(parsed.raises) == 2
    raise_names = {r.type_name for r in parsed.raises}
    assert raise_names == {"ValueError", "TypeError"}
    # Examples
    assert len(parsed.examples) == 1
    example = parsed.examples[0]
    assert isinstance(example, type(parsed.examples[0]))
    assert example.source.strip().startswith(">>>")
    # Meta
    assert parsed.meta is not None
    assert parsed.meta.short_description == "This function does something."

def test_parse_empty_docstring():
    parsed = parse("")
    assert isinstance(parsed, Docstring)
    assert parsed.meta.short_description == ""
    assert parsed.meta.long_description == ""
    assert parsed.params == []
    assert parsed.returns is None
    assert parsed.raises == []
    assert parsed.examples == []

def test_parse_invalid_docstring_raises_error():
    bad_doc = """
    This is a bad docstring
    Args:
        x int The argument without parentheses
    """
    with pytest.raises(ParseError):
        parse(bad_doc)
