import inspect
import pytest
from docstring_parser.numpydoc import parse, DocstringStyle, Docstring

def test_parse_basic_docstring():
    doc = """
    Short description.

    Long description line 1.
    Long description line 2.

    Parameters
    ----------
    x : int
        The first parameter.
    y : str
        The second parameter.

    Returns
    -------
    bool
        True if successful.
    """
    result = parse(doc)
    assert isinstance(result, Docstring)
    assert result.style == DocstringStyle.NUMPYDOC
    # Short and long description
    assert result.short_description == "Short description."
    assert result.long_description == "Long description line 1.\nLong description line 2."
    # Blank flags
    assert result.blank_after_short_description is False
    assert result.blank_after_long_description is False
    # Meta sections
    meta = {m.args[0]: m.description for m in result.meta}
    assert meta["param"] == "x : int\n    The first parameter.\ny : str\n    The second parameter."
    assert meta["returns"] == "bool\n    True if successful."

def test_parse_empty_and_no_sections():
    # Empty string should yield empty Docstring with no meta
    empty = ""
    empty_res = parse(empty)
    assert empty_res.short_description is None
    assert empty_res.long_description is None
    assert empty_res.meta == []

    # Docstring with only description, no sections
    desc_only = """
    Only a short description.
    """
    res = parse(desc_only)
    assert res.short_description == "Only a short description."
    assert res.long_description is None
    assert res.meta == []

def test_parse_boundary_and_invalid_section():
    # Docstring with a section that is not in DEFAULT_SECTIONS should be ignored
    doc = """
    Short.

    Unknown
    ------
    This should be ignored.

    Parameters
    ----------
    a : float
        Value.
    """
    res = parse(doc)
    # Only Parameters section should be parsed
    assert len(res.meta) == 1
    assert res.meta[0].args[0] == "param"
    assert "a : float" in res.meta[0].description
    # Ensure unknown section did not create a meta entry
    assert all(m.args[0] != "unknown" for m in res.meta)
