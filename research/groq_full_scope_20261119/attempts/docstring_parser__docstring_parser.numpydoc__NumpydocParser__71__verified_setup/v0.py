import pytest
from docstring_parser.numpydoc import NumpydocParser
from docstring_parser.common import DocstringStyle


def test_parse_basic():
    """Verify that a simple numpydoc docstring is parsed correctly."""
    doc = """
    Short description.

    Long description line 1.
    Long description line 2.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str, optional
        The second parameter.
    """
    parser = NumpydocParser()
    parsed = parser.parse(doc)

    # Short description
    assert parsed.short_description == "Short description."
    # Long description
    assert parsed.long_description == "Long description line 1.\nLong description line 2."
    # Blank lines detection
    assert parsed.blank_after_short_description is True
    assert parsed.blank_after_long_description is False
    # Meta sections
    assert len(parsed.meta) == 1
    params_section = parsed.meta[0]
    assert params_section.title == "Parameters"
    # Parameters parsed
    assert len(params_section.params) == 2
    param_names = {p.name for p in params_section.params}
    assert param_names == {"x", "y"}


def test_parse_empty():
    """Parsing an empty or whitespace-only docstring should return an empty Docstring."""
    parser = NumpydocParser()
    parsed = parser.parse("   \n  ")
    assert parsed.style == DocstringStyle.NUMPYDOC
    assert parsed.short_description is None
    assert parsed.long_description is None
    assert parsed.meta == []


def test_parse_unknown_section():
    """A docstring containing an unknown section title should raise KeyError."""
    doc = """
    Short description.

    UnknownSection
    --------------
    Some content.
    """
    parser = NumpydocParser()
    with pytest.raises(KeyError):
        parser.parse(doc)
