import pytest
from docstring_parser.google import parse
from docstring_parser.common import Docstring, DocstringParam, DocstringReturns, DocstringRaises, DocstringExample

def test_parse_basic_google_style():
    """Test parsing of a simple Google‑style docstring with params, returns, and raises."""
    docstring = """
    Short summary.

    Longer description that spans
    multiple lines.

    Args:
        x (int): The first argument.
        y (str, optional): The second argument. Defaults to 'foo'.

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        ValueError: If the input is invalid.
    """
    result = parse(docstring)
    assert isinstance(result, Docstring)
    # Summary and description
    assert result.short_description == "Short summary."
    assert result.long_description.strip() == "Longer description that spans multiple lines."
    # Parameters
    assert len(result.params) == 2
    param_x = next(p for p in result.params if p.arg_name == "x")
    assert param_x.type_name == "int"
    assert param_x.description == "The first argument."
    param_y = next(p for p in result.params if p.arg_name == "y")
    assert param_y.type_name == "str"
    assert param_y.description == "The second argument. Defaults to 'foo'."
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
    assert raise_item.description == "If the input is invalid."

def test_parse_with_examples_and_yields():
    """Test parsing of a docstring that includes examples and a yields section."""
    docstring = """
    Computes the Fibonacci sequence.

    Args:
        n (int): Number of terms.

    Yields:
        int: The next Fibonacci number.

    Examples:
        >>> fib = fibonacci(5)
        >>> list(fib)
        [0, 1, 1, 2, 3]
    """
    result = parse(docstring)
    assert isinstance(result, Docstring)
    # Yields
    assert len(result.yields) == 1
    yield_item = result.yields[0]
    assert yield_item.type_name == "int"
    assert yield_item.description == "The next Fibonacci number."
    # Examples
    assert len(result.examples) == 1
    example = result.examples[0]
    assert isinstance(example, DocstringExample)
    assert example.source.strip() == ">>> fib = fibonacci(5)\n>>> list(fib)"
    assert example.expected_output.strip() == "[0, 1, 1, 2, 3]"

def test_parse_invalid_docstring_raises_error():
    """Test that parsing an invalid Google‑style docstring raises ParseError."""
    invalid_docstring = """
    Args:
        x (int) The missing colon after type.
    """
    from docstring_parser.common import ParseError
    with pytest.raises(ParseError):
        parse(invalid_docstring)
