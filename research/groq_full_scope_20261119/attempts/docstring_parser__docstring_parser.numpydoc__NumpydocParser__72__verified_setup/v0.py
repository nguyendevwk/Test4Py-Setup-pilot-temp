import pytest
from docstring_parser.numpydoc import NumpydocParser, DocstringStyle

def test_parse_basic_docstring():
    """Verify that a simple numpydoc docstring is parsed correctly."""
    parser = NumpydocParser()
    doc = """
    Short description.

    Long description that spans
    multiple lines.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str, optional
        The second parameter.
    """
    result = parser.parse(doc)
    assert result.style == DocstringStyle.NUMPYDOC
    assert result.short_description == "Short description."
    assert result.long_description == "Long description that spans\nmultiple lines."
    assert result.blank_after_short_description is True
    assert result.blank_after_long_description is False
    # There should be two parameter entries
    params = [m for m in result.meta if hasattr(m, "name")]
    assert len(params) == 2
    names = {p.name for p in params}
    assert names == {"x", "y"}

def test_parse_empty_docstring():
    """An empty or None docstring should return an empty Docstring object."""
    parser = NumpydocParser()
    assert parser.parse("") == parser.parse(None)
    empty = parser.parse("")
    assert empty.short_description is None
    assert empty.long_description is None
    assert empty.meta == []

def test_parse_unknown_section_raises():
    """If the docstring contains a section title not in the parser's registry,
    a KeyError should be raised."""
    parser = NumpydocParser()
    bad_doc = """
    Short description.

    Unknown
    -------
    Some content that should trigger an error.
    """
    with pytest.raises(KeyError):
        parser.parse(bad_doc)
