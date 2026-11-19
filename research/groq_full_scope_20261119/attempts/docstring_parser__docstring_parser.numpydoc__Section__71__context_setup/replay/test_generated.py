import pytest
from docstring_parser.numpydoc import Section, DocstringMeta

def test_title_pattern_matches_and_non_matches():
    """Verify that the title_pattern correctly matches the section header."""
    section = Section("Parameters", "parameters")
    pattern = section.title_pattern
    # Should match exactly the header line with dashes
    assert pattern == r"^(Parameters)\s*?\n----------\s*$"
    # Use re to confirm matching
    import re
    assert re.match(pattern, "Parameters\n----------") is not None
    # Should not match if title differs
    assert re.match(pattern, "Returns\n-------") is None

def test_parse_returns_docstringmeta_with_cleaned_description():
    """Ensure parse yields a DocstringMeta with cleaned description."""
    section = Section("Returns", "returns")
    raw_text = "  This function returns a value.\n\n  It is useful.\n"
    # cleandoc would strip common indentation; here we simulate cleaned text
    cleaned = "This function returns a value.\n\nIt is useful."
    meta_iter = section.parse(cleaned)
    meta = next(meta_iter)
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["returns"]
    assert meta.description == cleaned.strip()
    # No more items
    with pytest.raises(StopIteration):
        next(meta_iter)

def test_parse_with_empty_text_returns_none_description():
    """When the section body is empty or whitespace, description should be None."""
    section = Section("Notes", "notes")
    empty_text = "   \n   "
    meta_iter = section.parse(empty_text)
    meta = next(meta_iter)
    assert isinstance(meta, DocstringMeta)
    assert meta.args == ["notes"]
    assert meta.description is None
