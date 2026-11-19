import inspect
import pytest
from docstring_parser.numpydoc import NumpydocParser
from docstring_parser.common import DocstringStyle, DocstringMeta, DocstringParam, DocstringReturns, DocstringRaises

def test_parse_basic_docstring(tmp_path):
    """Verify that a simple numpydoc docstring is parsed correctly."""
    doc = """
    Short description.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str
        The second parameter.

    Returns
    -------
    bool
        Result of the operation.
    """
    parser = NumpydocParser()
    result = parser.parse(doc)

    # Short and long descriptions
    assert result.short_description == "Short description."
    assert result.long_description == "Long description that spans\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False

    # Meta sections
    meta_titles = [m.title for m in result.meta]
    assert "Parameters" in meta_titles
    assert "Returns" in meta_titles

    # Parameters section
    params = next(m for m in result.meta if m.title == "Parameters")
    assert isinstance(params, DocstringMeta)
    assert len(params.params) == 2
    assert params.params[0].arg_name == "x"
    assert params.params[0].type_name == "int"
    assert params.params[0].description == "The first parameter."
    assert params.params[1].arg_name == "y"
    assert params.params[1].type_name == "str"
    assert params.params[1].description == "The second parameter."

    # Returns section
    returns = next(m for m in result.meta if m.title == "Returns")
    assert isinstance(returns, DocstringMeta)
    assert len(returns.returns) == 1
    assert returns.returns[0].type_name == "bool"
    assert returns.returns[0].description == "Result of the operation."

def test_parse_no_sections(tmp_path):
    """Verify that a docstring with no section headers is parsed as description only."""
    doc = """
    Only a short description.
    """
    parser = NumpydocParser()
    result = parser.parse(doc)

    assert result.short_description == "Only a short description."
    assert result.long_description is None
    assert result.meta == []

def test_parse_unknown_section_raises():
    """Verify that an unknown section title raises a KeyError."""
    doc = """
    Short description.

    Unknown
    ------
    Some content.
    """
    parser = NumpydocParser()
    with pytest.raises(KeyError):
        parser.parse(doc)
