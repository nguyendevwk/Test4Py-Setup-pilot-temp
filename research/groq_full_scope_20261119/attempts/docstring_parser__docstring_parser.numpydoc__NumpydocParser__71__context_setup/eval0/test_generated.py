import inspect
import textwrap
import pytest
from docstring_parser.numpydoc import NumpydocParser, DocstringStyle, DocstringMeta, DocstringExample, DocstringParam, DocstringRaises, DocstringReturns


def test_parse_basic_description_and_examples():
    """Verify that a simple docstring with a short description, long description, and an examples section is parsed correctly."""
    doc = textwrap.dedent("""
        Short description.

        This is a long description that spans
        multiple lines and provides more detail.

        Examples
        --------
        >>> 1 + 1
        2
        >>> 2 * 3
        6
    """)
    parser = NumpydocParser()
    result = parser.parse(doc)

    # Short and long description
    assert result.short_description == "Short description."
    assert result.long_description == "This is a long description that spans\nmultiple lines and provides more detail."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False

    # Example parsing
    examples = [m for m in result.meta if isinstance(m, DocstringExample)]
    assert len(examples) == 1
    example = examples[0]
    assert example.args == ["examples"]
    assert example.snippet == ">>> 1 + 1\n>>> 2 * 3"
    assert example.description == "2\n6"


def test_parse_parameters_and_returns_and_raises():
    """Verify that parameter, return, and raises sections are parsed into the correct meta objects."""
    doc = textwrap.dedent("""
        Parameters
        ----------
        x : int
            The first integer.
        y : float, optional
            The second value. Defaults to 0.0.

        Returns
        -------
        result : int
            The sum of x and y.

        Raises
        ------
        ValueError
            If x is negative.
    """)
    parser = NumpydocParser()
    result = parser.parse(doc)

    # Parameters
    params = [m for m in result.meta if isinstance(m, DocstringParam)]
    assert len(params) == 2
    param_x, param_y = params
    assert param_x.args == ["parameters", "x"]
    assert param_x.type_name == "int"
    assert param_x.is_optional is False
    assert param_x.default is None
    assert param_x.description == "The first integer."

    assert param_y.args == ["parameters", "y"]
    assert param_y.type_name == "float"
    assert param_y.is_optional is True
    assert param_y.default == "0.0"
    assert param_y.description == "The second value."

    # Returns
    returns = [m for m in result.meta if isinstance(m, DocstringReturns)]
    assert len(returns) == 1
    ret = returns[0]
    assert ret.args == ["returns"]
    assert ret.type_name == "int"
    assert ret.return_name == "result"
    assert ret.description == "The sum of x and y."

    # Raises
    raises = [m for m in result.meta if isinstance(m, DocstringRaises)]
    assert len(raises) == 1
    raise_obj = raises[0]
    assert raise_obj.args == ["raises", "ValueError"]
    assert raise_obj.type_name == "ValueError"
    assert raise_obj.description == "If x is negative."


def test_parse_empty_and_invalid_sections():
    """Verify that an empty docstring returns an empty Docstring and that unknown sections are ignored gracefully."""
    parser = NumpydocParser()

    # Empty docstring
    empty_result = parser.parse("")
    assert empty_result.short_description is None
    assert empty_result.long_description is None
    assert empty_result.meta == []

    # Docstring with an unrecognized section header
    doc = textwrap.dedent("""
        This is a normal description.

        Unknown
        ------
        Some content that should be ignored.
    """)
    result = parser.parse(doc)
    assert result.short_description == "This is a normal description."
    assert result.long_description is None
    # No meta objects should be created for the unknown section
    assert all(not isinstance(m, DocstringMeta) for m in result.meta)
